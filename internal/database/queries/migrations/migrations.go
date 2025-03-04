package migrations

import (
	"context"
	"database/sql"
	"log"

	"akingbee/internal/database/queries/migrations/M0001"
	"akingbee/internal/database/queries/migrations/M0002"
	"akingbee/internal/database/queries/migrations/M0003"
	"akingbee/internal/database/queries/migrations/M0004"
	"akingbee/internal/database/queries/migrations/M0005"
)

func Upgrade(ctx context.Context, dbClient *sql.DB) {
	log.Print("Running migrations")

	err := M0001.Upgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}

	err = M0002.Upgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}

	err = M0003.Upgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}

	err = M0004.Upgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}

	err = M0005.Upgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}
}

func Downgrade(ctx context.Context, dbClient *sql.DB) {
	err := M0002.Downgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}

	err = M0001.Downgrade(ctx, dbClient)
	if err != nil {
		log.Printf("Migration failed: %s", err)
		return
	}
}
