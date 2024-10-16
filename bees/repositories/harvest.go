package repositories

import (
	"akingbee/bees/models"
	"akingbee/internal/database"
	"context"
	"fmt"
	"log"

	"github.com/google/uuid"
)

const queryCreateHarvest = `
	INSERT INTO HARVEST (
		PUBLIC_ID, DATE, QUANTITY, HIVE_ID
	) VALUES (
		$1, 
		$2,
		$3,
		(SELECT HIVE.ID WHERE HIVE.PUBLIC_ID=$4)
	)
`

func CreateHarvest(ctx context.Context, harvest *models.Harvest) error {
	db := database.GetDb()

	_, err := db.ExecContext(
		ctx,
		queryCreateHarvest,
		harvest.PublicId,
		harvest.Date,
		harvest.Quantity,
		harvest.HivePublicId,
	)

	return err
}

const queryGetHarvest = `
	SELECT HARVEST.PUBLIC_ID, DATE, QUANTITY, HIVE.PUBLIC_ID
	FROM HARVEST
	JOIN HIVE ON HIVE.ID=HARVEST.HIVE_ID
`

func GetHarvests(ctx context.Context, hivePublicId *uuid.UUID) ([]models.Harvest, error) {
	var harvests []models.Harvest

	db := database.GetDb()

	rows, err := db.QueryContext(
		ctx,
		fmt.Sprintf("%s WHERE HIVE.PUBLIC_ID=$1", queryGetHarvest),
		hivePublicId,
	)

	if err != nil {
		log.Printf("Error while querying harvest: %s", err)
		return nil, err
	}

	for rows.Next() {
		var harvest models.Harvest

		err := rows.Scan(
			&harvest.PublicId,
			&harvest.Date,
			&harvest.Quantity,
			&harvest.HivePublicId,
		)
		if err != nil {
			return nil, err
		}

		harvests = append(harvests, harvest)
	}

	return harvests, err
}

const queryDeleteHarvest = `
	DELETE FROM HARVEST
	WHERE PUBLIC_ID=$1
`

func DeleteHarvest(ctx context.Context, harvest *models.Harvest) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryDeleteHarvest, harvest.PublicId)
	return err
}
