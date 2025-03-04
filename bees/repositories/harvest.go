package repositories

import (
	"context"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/internal/database"
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
	db := database.GetDB()

	_, err := db.ExecContext(
		ctx,
		queryCreateHarvest,
		harvest.PublicID,
		harvest.Date,
		harvest.Quantity,
		harvest.HivePublicID,
	)

	return err
}

const queryGetHarvest = `
	SELECT HARVEST.PUBLIC_ID, DATE, QUANTITY, HIVE.PUBLIC_ID
	FROM HARVEST
	JOIN HIVE ON HIVE.ID=HARVEST.HIVE_ID
`

func GetHarvests(ctx context.Context, hivePublicID *uuid.UUID) ([]models.Harvest, error) {
	var harvests []models.Harvest

	db := database.GetDB()

	rows, err := db.QueryContext(
		ctx,
		queryGetHarvest+" WHERE HIVE.PUBLIC_ID=$1 ORDER BY HARVEST.DATE DESC, HARVEST.DATE_CREATION DESC",
		hivePublicID,
	)

	if err != nil {
		log.Printf("Error while querying harvest: %s", err)

		return nil, err
	}

	for rows.Next() {
		var harvest models.Harvest

		err := rows.Scan(
			&harvest.PublicID,
			&harvest.Date,
			&harvest.Quantity,
			&harvest.HivePublicID,
		)
		if err != nil {
			return nil, err
		}

		harvests = append(harvests, harvest)
	}

	if rows.Err() != nil {
		return nil, fmt.Errorf("rows closed unexpectedly: %w", rows.Err())
	}

	return harvests, err
}

func GetHarvest(ctx context.Context, harvestPublicID *uuid.UUID) (*models.Harvest, error) {
	db := database.GetDB()

	rows, err := db.QueryContext(
		ctx,
		queryGetHarvest+" WHERE HARVEST.PUBLIC_ID=$1",
		harvestPublicID,
	)

	defer database.CloseRows(rows)

	if err != nil {
		log.Printf("Error while querying harvest: %s", err)

		return nil, err
	}

	var harvest models.Harvest

	rows.Next()
	err = rows.Scan(
		&harvest.PublicID,
		&harvest.Date,
		&harvest.Quantity,
		&harvest.HivePublicID,
	)

	if rows.Err() != nil {
		return nil, fmt.Errorf("rows closed unexpectedly: %w", rows.Err())
	}

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
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryDeleteHarvest, harvest.PublicID)

	return err
}
