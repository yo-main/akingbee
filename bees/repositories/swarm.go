package repositories

import (
	"akingbee/bees/models"
	"akingbee/internal/database"
	"context"
	"fmt"
	"github.com/google/uuid"
	"log"
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
	db := database.GetDb()

	_, err := db.ExecContext(ctx, queryCreateSwarm, swarm.PublicId, swarm.Year, swarm.Health)

	return err
}

const queryUpdateSwarm = `
	UPDATE SWARM 
	SET YEAR=$1, HEALTH=$2
	WHERE PUBLIC_ID=$3
`

func UpdateSwarm(ctx context.Context, swarm *models.Swarm) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryUpdateSwarm, swarm.Year, swarm.Health, swarm.PublicId)
	return err
}

const queryDeleteSwarm = `
	DELETE FROM SWARM 
	WHERE PUBLIC_ID=$1
`

func DeleteSwarm(ctx context.Context, swarm *models.Swarm) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryDeleteSwarm, swarm.PublicId)
	return err
}

func GetSwarmValues(ctx context.Context, value string, userId *uuid.UUID) []string {
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

	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetSwarmValue, userId)

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
