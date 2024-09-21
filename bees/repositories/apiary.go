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
	WHERE USERS.PUBLIC_ID=$1
`

func GetApiary(ctx context.Context, ownerId *uuid.UUID) ([]models.Apiary, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetApiary, ownerId)
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
