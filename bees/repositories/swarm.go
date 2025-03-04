package repositories

import (
	"context"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/internal/database"
)

const queryCreateSwarm = `
	INSERT INTO SWARM (
		public_id, year, health
	) VALUES (
		$1, 
		$2,
		$3
	)
`

func CreateSwarm(ctx context.Context, swarm *models.Swarm) error {
	db := database.GetDB()

	_, err := db.ExecContext(ctx, queryCreateSwarm, swarm.PublicID, swarm.Year, swarm.Health)

	return err
}

const queryUpdateSwarm = `
	UPDATE SWARM 
	SET YEAR=$1, HEALTH=$2
	WHERE PUBLIC_ID=$3
`

func UpdateSwarm(ctx context.Context, swarm *models.Swarm) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryUpdateSwarm, swarm.Year, swarm.Health, swarm.PublicID)

	return err
}

const queryDeleteSwarm = `
	DELETE FROM SWARM 
	WHERE PUBLIC_ID=$1
`

func DeleteSwarm(ctx context.Context, swarm *models.Swarm) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryDeleteSwarm, swarm.PublicID)

	return err
}

func GetSwarmValues(ctx context.Context, value string, userID *uuid.UUID) []string {
	results := []string{}

	if value != "health" {
		log.Printf("Wrong choice of value: %s", value)
		return results
	}

	queryGetSwarmValue := fmt.Sprintf(`
		SELECT DISTINCT %s
		FROM SWARM
		JOIN HIVE ON SWARM.ID=HIVE.SWARM_ID
		JOIN USERS ON USERS.ID=HIVE.USER_ID
		WHERE USERS.PUBLIC_ID=$1
	`, value)

	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetSwarmValue, userID)

	if err != nil {
		log.Printf("Error executing query: %s", err)
		return nil
	}

	defer database.CloseRows(rows)

	for rows.Next() {
		var value string
		err = rows.Scan(&value)

		if err != nil {
			log.Printf("Error while scanning row: %s", err)
			return nil
		}

		results = append(results, value)
	}

	if rows.Err() != nil {
		log.Printf("rows closed unexpectedly: %s", rows.Err())
		return nil
	}

	return results
}
