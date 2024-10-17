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
		(SELECT HIVE.ID FROM HIVE WHERE HIVE.PUBLIC_ID=$4)
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
		fmt.Sprintf("%s WHERE HIVE.PUBLIC_ID=$1 ORDER BY HARVEST.DATE DESC, HARVEST.DATE_CREATION DESC", queryGetHarvest),
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

func GetHarvest(ctx context.Context, harvestPublicId *uuid.UUID) (*models.Harvest, error) {
	db := database.GetDb()

	rows, err := db.QueryContext(
		ctx,
		fmt.Sprintf("%s WHERE HARVEST.PUBLIC_ID=$1", queryGetHarvest),
		harvestPublicId,
	)
	defer rows.Close()

	if err != nil {
		log.Printf("Error while querying harvest: %s", err)
		return nil, err
	}

	var harvest models.Harvest

	rows.Next()
	err = rows.Scan(
		&harvest.PublicId,
		&harvest.Date,
		&harvest.Quantity,
		&harvest.HivePublicId,
	)
	if err != nil {
		return nil, err
	}

	return &harvest, err
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
