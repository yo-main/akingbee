package repositories

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/internal/database"
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
	db := database.GetDB()

	apiaryPublicID := hive.GetApiaryPublicID()
	swarmPublicID := hive.GetSwarmPublicID()

	_, err := db.ExecContext(
		ctx, queryCreateHive, hive.PublicID, hive.Name, hive.Beekeeper, apiaryPublicID, swarmPublicID, hive.User,
	)

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
	db := database.GetDB()

	apiaryPublicID := hive.GetApiaryPublicID()
	swarmPublicID := hive.GetSwarmPublicID()

	_, err := db.ExecContext(ctx, queryUpdateHive, hive.Name, hive.Beekeeper, apiaryPublicID, swarmPublicID, hive.PublicID)

	return err
}

const queryDeleteHive = `
	DELETE FROM HIVE 
	WHERE PUBLIC_ID=$1
`

func DeleteHive(ctx context.Context, hive *models.Hive) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryDeleteHive, hive.PublicID)

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
		&hive.PublicID,
		&hive.Name,
		&hive.Beekeeper,
		&apiary.PublicID,
		&apiary.Name,
		&apiary.Location,
		&apiary.HoneyKind,
		&apiary.HiveCount,
		&swarm.PublicID,
		&swarm.Year,
		&swarm.Health,
		&apiary.User,
		&hive.User,
	)

	if err != nil {
		return nil, fmt.Errorf("could not build Hive from result: %w", err)
	}

	if apiary.PublicID != uuid.Nil {
		hive.SetApiary(&apiary)
	}

	if swarm.PublicID != uuid.Nil {
		hive.SetSwarm(&swarm)
	}

	return &hive, nil
}

func GetHives(ctx context.Context, userID *uuid.UUID) ([]*models.Hive, error) {
	db := database.GetDB()
	query := queryGetHives + " WHERE USERS.PUBLIC_ID=$1 ORDER BY HIVE.DATE_CREATION DESC"
	rows, err := db.QueryContext(ctx, query, userID)

	if err != nil {
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

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

func GetHive(ctx context.Context, hivePublicID *uuid.UUID) (*models.Hive, error) {
	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetHives+" WHERE HIVE.PUBLIC_ID=$1", hivePublicID)

	if err != nil {
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

	rows.Next()
	hive, err := scanHive(rows)

	if err != nil {
		return nil, fmt.Errorf("could not build Hive from result: %w", err)
	}

	return hive, err
}

func GetHiveValues(ctx context.Context, value string, userID *uuid.UUID) []string {
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

	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetHiveValue, userID)

	if err != nil {
		log.Printf("Error executing query: %s", err)
		return nil
	}

	defer database.CloseRows(rows)

	for rows.Next() {
		var value string
		err = rows.Scan(&value)

		if err != nil {
			log.Println("Could not scan value correctly: %w", err)
			return nil
		}

		results = append(results, value)
	}

	if rows.Err() != nil {
		log.Println("rows closed unexpectedly: %w", rows.Err())
		return nil
	}

	return results
}
