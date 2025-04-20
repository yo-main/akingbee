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
	"akingbee/internal/database/queries/migrations/M0006"
)

func Upgrade(ctx context.Context, dbClient *sql.DB) {
	log.Print("Running migrations")

	err := M0001.Upgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0002.Upgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0003.Upgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0004.Upgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0005.Upgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0006.Upgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}
}

func Downgrade(ctx context.Context, dbClient *sql.DB) {
	err := M0006.Downgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0005.Downgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0004.Downgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0003.Downgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0002.Downgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	err = M0001.Downgrade(ctx, dbClient)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}
}
