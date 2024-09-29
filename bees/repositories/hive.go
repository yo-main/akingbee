package repositories

import (
	"akingbee/bees/models"
	"akingbee/internal/database"
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"

	"github.com/google/uuid"
)

const queryCreateHive = `
	INSERT INTO HIVE (
		public_id, name, condition, apiary_id, swarm_id, owner_id
	) VALUES (
		$1, 
		$2,
		$3,
		(SELECT APIARY.ID FROM APIARY WHERE APIARY.PUBLIC_ID=$4),
		(SELECT SWARM.ID FROM SWARM WHERE SWARM.PUBLIC_ID=$5),
		(SELECT USERS.ID FROM USERS WHERE USERS.PUBLIC_ID=$6)
	)
`

func CreateHive(ctx context.Context, hive *models.Hive) error {
	db := database.GetDb()

	var apiaryPublicId uuid.UUID
	if hive.Apiary != nil {
		apiaryPublicId = hive.Apiary.PublicId
	}
	var swarmPublicId uuid.UUID
	if hive.Swarm != nil {
		swarmPublicId = hive.Swarm.PublicId
	}
	_, err := db.ExecContext(ctx, queryCreateHive, hive.PublicId, hive.Name, hive.Condition, apiaryPublicId, swarmPublicId, hive.Owner)

	return err
}

const queryUpdateHive = `
	UPDATE HIVE 
	SET 
		NAME=$1,
		CONDITION=$2,
		APIARY_ID=(SELECT APIARY.ID FROM APIARY WHERE APIARY.PUBLIC_ID=$3),
		SWARM_ID=(SELECT SWARM.ID FROM SWARM WHERE SWARM.PUBLIC_ID=$4)
	WHERE PUBLIC_ID=$5
`

func UpdateHive(ctx context.Context, hive *models.Hive) error {
	db := database.GetDb()
	var apiaryPublicId uuid.UUID
	if hive.Apiary != nil {
		apiaryPublicId = hive.Apiary.PublicId
	}
	var swarmPublicId uuid.UUID
	if hive.Swarm != nil {
		swarmPublicId = hive.Swarm.PublicId
	}
	_, err := db.ExecContext(ctx, queryUpdateHive, hive.Name, hive.Condition, apiaryPublicId, swarmPublicId, hive.PublicId)
	return err
}

const queryDeleteHive = `
	DELETE FROM HIVE 
	WHERE PUBLIC_ID=$1
`

func DeleteHive(ctx context.Context, hive *models.Hive) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryDeleteHive, hive.PublicId)
	return err
}

const queryGetHives = `
	WITH APIARIES AS (
		SELECT
			APIARY.ID,
			APIARY.PUBLIC_ID, 
			APIARY.NAME,
			APIARY.LOCATION,
			APIARY.HONEY_KIND,
			COUNT(*) AS HIVE_COUNT
		FROM APIARY
		JOIN USERS ON USERS.ID=APIARY.OWNER_ID
		JOIN HIVE ON HIVE.APIARY_ID=APIARY.ID
		GROUP BY 1, 2, 3, 4, 5
	)
	SELECT 
		HIVE.PUBLIC_ID, 
		HIVE.NAME,
		HIVE.CONDITION,
		APIARIES.PUBLIC_ID,
		COALESCE(APIARIES.NAME, ''),
		COALESCE(APIARIES.LOCATION, ''),
		COALESCE(APIARIES.HONEY_KIND, ''),
		COALESCE(APIARIES.HIVE_COUNT, 0),
		SWARM.PUBLIC_ID,
		COALESCE(SWARM.YEAR, 0),
		COALESCE(SWARM.HEALTH, ''),
		USERS.PUBLIC_ID,
		USERS.PUBLIC_ID
	FROM HIVE
	JOIN USERS ON USERS.ID=HIVE.OWNER_ID
	LEFT JOIN APIARIES ON APIARIES.ID=HIVE.APIARY_ID
	LEFT JOIN SWARM ON SWARM.ID=HIVE.SWARM_ID
`

func scanHive(rows *sql.Rows) (*models.Hive, error) {
	var apiary models.Apiary
	var hive models.Hive
	var swarm models.Swarm
	err := rows.Scan(
		&hive.PublicId,
		&hive.Name,
		&hive.Condition,
		&apiary.PublicId,
		&apiary.Name,
		&apiary.Location,
		&apiary.HoneyKind,
		&apiary.HiveCount,
		&swarm.PublicId,
		&swarm.Year,
		&swarm.Health,
		&apiary.Owner,
		&hive.Owner,
	)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("Could not build Hive from result: %s", err))
	}
	if apiary.PublicId != uuid.Nil {
		hive.Apiary = &apiary
	}
	if swarm.PublicId != uuid.Nil {
		hive.Swarm = &swarm
	}
	return &hive, nil
}

func GetHives(ctx context.Context, ownerId *uuid.UUID) ([]*models.Hive, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, fmt.Sprintf("%s WHERE USERS.PUBLIC_ID=$1 ORDER BY HIVE.DATE_CREATION DESC", queryGetHives), ownerId)
	defer rows.Close()

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	hives := []*models.Hive{}

	for rows.Next() {
		hive, err := scanHive(rows)
		if err != nil {
			return nil, err
		}
		hives = append(hives, hive)
	}

	return hives, err
}

func GetHive(ctx context.Context, hivePublicId *uuid.UUID) (*models.Hive, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, fmt.Sprintf("%s WHERE HIVE.PUBLIC_ID=$1", queryGetHives), hivePublicId)
	defer rows.Close()

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	rows.Next()
	hive, err := scanHive(rows)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("Could not build Hive from result: %s", err))
	}

	return hive, err
}

func GetHiveValues(ctx context.Context, value string, ownerId *uuid.UUID) []string {
	results := []string{}

	if value != "condition" {
		log.Printf("Wrong choice of value: %s", value)
		return results
	}

	queryGetHiveValue := fmt.Sprintf(`
		SELECT DISTINCT %s
		FROM HIVE
		JOIN USERS ON USERS.ID=HIVE.OWNER_ID
		WHERE USERS.PUBLIC_ID=$1
	`, value)

	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetHiveValue, ownerId)
	defer rows.Close()

	if err != nil {
		log.Printf("Error executing query: %s", err)
		return nil
	}

	for rows.Next() {
		var value string
		rows.Scan(&value)
		results = append(results, value)
	}

	return results
}
