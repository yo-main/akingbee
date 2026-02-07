package repositories

import (
	"context"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/internal/database"
)

const queryCreateApiary = `
	INSERT INTO APIARY (
		public_id, name, location, honey_kind, user_id
	) VALUES (
		$1, $2, $3, $4, (SELECT USERS.ID FROM USERS WHERE USERS.PUBLIC_ID=$5)
	)
`

func CreateApiary(ctx context.Context, apiary *models.Apiary) error {
	db := database.GetDB()
	_, err := db.ExecContext(
		ctx, queryCreateApiary, apiary.PublicID, apiary.Name, apiary.Location, apiary.HoneyKind, apiary.User,
	)

	return err
}

const queryUpdateApiary = `
	UPDATE APIARY 
	SET NAME=$1, LOCATION=$2, HONEY_KIND=$3
	WHERE PUBLIC_ID=$4
`

func UpdateApiary(ctx context.Context, apiary *models.Apiary) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryUpdateApiary, apiary.Name, apiary.Location, apiary.HoneyKind, apiary.PublicID)

	return err
}

const queryDeleteApiary = `
	DELETE FROM APIARY 
	WHERE PUBLIC_ID=$1
`

func DeleteApiary(ctx context.Context, apiary *models.Apiary) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryDeleteApiary, apiary.PublicID)

	return fmt.Errorf("could not delete apiary: %w", err)
}

const queryGetApiaries = `
	SELECT 
		APIARY.PUBLIC_ID, 
		APIARY.NAME,
		APIARY.LOCATION,
		APIARY.HONEY_KIND,
		USERS.PUBLIC_ID, 
		COUNT(HIVE.ID) AS HIVE_COUNT
	FROM APIARY
	JOIN USERS ON USERS.ID=APIARY.USER_ID
	LEFT JOIN HIVE ON HIVE.APIARY_ID=APIARY.ID
	WHERE USERS.PUBLIC_ID=$1
	GROUP BY 1, 2, 3, 4, 5
	ORDER BY APIARY.DATE_CREATION DESC
`

func GetApiaries(ctx context.Context, userID *uuid.UUID) ([]models.Apiary, error) {
	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetApiaries, userID)

	if err != nil {
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

	apiaries := []models.Apiary{}

	for rows.Next() {
		var apiary models.Apiary
		err = rows.Scan(&apiary.PublicID, &apiary.Name, &apiary.Location, &apiary.HoneyKind, &apiary.User, &apiary.HiveCount)

		if err != nil {
			return nil, fmt.Errorf("could not build Apiary from result: %w", err)
		}

		apiaries = append(apiaries, apiary)
	}

	if rows.Err() != nil {
		return nil, fmt.Errorf("rows closed unexpectedly: %w", rows.Err())
	}

	return apiaries, nil
}

const queryGetApiary = `
	SELECT 
		APIARY.PUBLIC_ID, 
		APIARY.NAME,
		APIARY.LOCATION,
		APIARY.HONEY_KIND,
		USERS.PUBLIC_ID, 
		2 AS HIVE_COUNT
	FROM APIARY
	JOIN USERS ON USERS.ID=APIARY.USER_ID
	WHERE APIARY.PUBLIC_ID=$1
`

func GetApiary(ctx context.Context, apiaryPublicID *uuid.UUID) (*models.Apiary, error) {
	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetApiary, apiaryPublicID)

	if err != nil {
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

	var apiary models.Apiary

	rows.Next()
	err = rows.Scan(&apiary.PublicID, &apiary.Name, &apiary.Location, &apiary.HoneyKind, &apiary.User, &apiary.HiveCount)

	if err != nil {
		return nil, fmt.Errorf("could not build Apiary from result: %w", err)
	}

	if rows.Err() != nil {
		return nil, fmt.Errorf("connection closed unexpectedly: %w", rows.Err())
	}

	return &apiary, nil
}

func GetApiaryValues(ctx context.Context, value string, userID *uuid.UUID) []string {
	results := []string{}

	if !(value == "location" || value == "honey_kind") {
		log.Printf("Wrong choice of value: %s", value)

		return results
	}

	queryGetApiaryValue := fmt.Sprintf(`
		SELECT DISTINCT %s
		FROM APIARY
		JOIN USERS ON USERS.ID=APIARY.USER_ID
		WHERE USERS.PUBLIC_ID=$1
	`, value)

	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetApiaryValue, userID)

	if err != nil {
		log.Printf("Error executing query: %s", err)

		return nil
	}

	defer database.CloseRows(rows)

	for rows.Next() {
		var value string
		err = rows.Scan(&value)

		if err != nil {
			log.Println("Could not scan row: %w", err)

			return nil
		}

		results = append(results, value)
	}

	if rows.Err() != nil {
		return nil
	}

	return results
}
