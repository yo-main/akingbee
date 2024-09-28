package repositories

import (
	"akingbee/bees/models"
	"akingbee/internal/database"
	"context"
	"errors"
	"fmt"
	"log"

	"github.com/google/uuid"
)

const queryCreateApiary = `
	INSERT INTO APIARY (
		public_id, name, location, honey_kind, owner_id
	) VALUES (
		$1, $2, $3, $4, (SELECT USERS.ID FROM USERS WHERE USERS.PUBLIC_ID=$5)
	)
`

func CreateApiary(ctx context.Context, apiary *models.Apiary) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryCreateApiary, apiary.PublicId, apiary.Name, apiary.Location, apiary.HoneyKind, apiary.Owner)

	return err
}

const queryUpdateApiary = `
	UPDATE APIARY 
	SET NAME=$1, LOCATION=$2, HONEY_KIND=$3
	WHERE PUBLIC_ID=$4
`

func UpdateApiary(ctx context.Context, apiary *models.Apiary) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryUpdateApiary, apiary.Name, apiary.Location, apiary.HoneyKind, apiary.PublicId)
	return err
}

const queryDeleteApiary = `
	DELETE FROM APIARY 
	WHERE PUBLIC_ID=$1
`

func DeleteApiary(ctx context.Context, apiary *models.Apiary) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryDeleteApiary, apiary.PublicId)
	return err
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
	JOIN USERS ON USERS.ID=APIARY.OWNER_ID
	LEFT JOIN HIVE ON HIVE.APIARY_ID=APIARY.ID
	WHERE USERS.PUBLIC_ID=$1
	GROUP BY 1, 2, 3, 4, 5
	ORDER BY APIARY.DATE_CREATION DESC
`

func GetApiaries(ctx context.Context, ownerId *uuid.UUID) ([]models.Apiary, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetApiaries, ownerId)
	defer rows.Close()

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	apiaries := []models.Apiary{}

	for rows.Next() {
		var apiary models.Apiary
		err = rows.Scan(&apiary.PublicId, &apiary.Name, &apiary.Location, &apiary.HoneyKind, &apiary.Owner, &apiary.HiveCount)
		if err != nil {
			return nil, errors.New(fmt.Sprintf("Could not build Apiary from result: %s", err))
		}
		apiaries = append(apiaries, apiary)
	}

	return apiaries, err
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
	JOIN USERS ON USERS.ID=APIARY.OWNER_ID
	WHERE APIARY.PUBLIC_ID=$1
`

func GetApiary(ctx context.Context, apiaryPublicId *uuid.UUID) (*models.Apiary, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetApiary, apiaryPublicId)
	defer rows.Close()

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	var apiary models.Apiary
	rows.Next()
	err = rows.Scan(&apiary.PublicId, &apiary.Name, &apiary.Location, &apiary.HoneyKind, &apiary.Owner, &apiary.HiveCount)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("Could not build Apiary from result: %s", err))
	}

	return &apiary, err
}

func GetApiaryValues(ctx context.Context, value string, ownerId *uuid.UUID) []string {
	results := []string{}

	if !(value == "location" || value == "honey_kind") {
		log.Printf("Wrong choice of value: %s", value)
		return results
	}

	queryGetApiaryValue := fmt.Sprintf(`
		SELECT DISTINCT %s
		FROM APIARY
		JOIN USERS ON USERS.ID=APIARY.OWNER_ID
		WHERE USERS.PUBLIC_ID=$1
	`, value)

	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetApiaryValue, ownerId)
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
