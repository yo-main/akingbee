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
		public_id, name, beekeeper, apiary_id, swarm_id, user_id
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

	apiaryPublicId := hive.GetApiaryPublicId()
	swarmPublicId := hive.GetSwarmPublicId()

	_, err := db.ExecContext(ctx, queryCreateHive, hive.PublicId, hive.Name, hive.Beekeeper, apiaryPublicId, swarmPublicId, hive.User)

	return err
}

const queryUpdateHive = `
	UPDATE HIVE 
	SET 
		NAME=$1,
		BEEKEEPER=$2,
		APIARY_ID=(SELECT APIARY.ID FROM APIARY WHERE APIARY.PUBLIC_ID=$3),
		SWARM_ID=(SELECT SWARM.ID FROM SWARM WHERE SWARM.PUBLIC_ID=$4)
	WHERE PUBLIC_ID=$5
`

func UpdateHive(ctx context.Context, hive *models.Hive) error {
	db := database.GetDb()

	apiaryPublicId := hive.GetApiaryPublicId()
	swarmPublicId := hive.GetSwarmPublicId()

	_, err := db.ExecContext(ctx, queryUpdateHive, hive.Name, hive.Beekeeper, apiaryPublicId, swarmPublicId, hive.PublicId)
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
		JOIN USERS ON USERS.ID=APIARY.USER_ID
		JOIN HIVE ON HIVE.APIARY_ID=APIARY.ID
		GROUP BY 1, 2, 3, 4, 5
	)
	SELECT 
		HIVE.PUBLIC_ID, 
		HIVE.NAME,
		HIVE.BEEKEEPER,
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
	JOIN USERS ON USERS.ID=HIVE.USER_ID
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
		&hive.Beekeeper,
		&apiary.PublicId,
		&apiary.Name,
		&apiary.Location,
		&apiary.HoneyKind,
		&apiary.HiveCount,
		&swarm.PublicId,
		&swarm.Year,
		&swarm.Health,
		&apiary.User,
		&hive.User,
	)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("Could not build Hive from result: %s", err))
	}
	if apiary.PublicId != uuid.Nil {
		hive.SetApiary(&apiary)
	}
	if swarm.PublicId != uuid.Nil {
		hive.SetSwarm(&swarm)
	}

	return &hive, nil
}

func GetHives(ctx context.Context, userId *uuid.UUID) ([]*models.Hive, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, fmt.Sprintf("%s WHERE USERS.PUBLIC_ID=$1 ORDER BY HIVE.DATE_CREATION DESC", queryGetHives), userId)

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	defer rows.Close()

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

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	defer rows.Close()

	rows.Next()
	hive, err := scanHive(rows)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("Could not build Hive from result: %s", err))
	}

	return hive, err
}

func GetHiveValues(ctx context.Context, value string, userId *uuid.UUID) []string {
	results := []string{}

	if value != "beekeeper" {
		log.Printf("Wrong choice of value: %s", value)
		return results
	}

	queryGetHiveValue := fmt.Sprintf(`
		SELECT DISTINCT %s
		FROM HIVE
		JOIN USERS ON USERS.ID=HIVE.USER_ID
		WHERE USERS.PUBLIC_ID=$1
	`, value)

	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetHiveValue, userId)

	if err != nil {
		log.Printf("Error executing query: %s", err)
		return nil
	}

	defer rows.Close()

	for rows.Next() {
		var value string
		rows.Scan(&value)
		results = append(results, value)
	}

	return results
}
