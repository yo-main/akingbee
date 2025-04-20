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

	dbClient.ExecContext(ctx, "CREATE TABLE IF NOT EXISTS migrations(version INTEGER NOT NULL);")

	currentVersion := getCurrentVersion(ctx, dbClient)

	execUpgrade(M0001.Upgrade, ctx, dbClient, &currentVersion, 1)
	execUpgrade(M0002.Upgrade, ctx, dbClient, &currentVersion, 2)
	execUpgrade(M0003.Upgrade, ctx, dbClient, &currentVersion, 3)
	execUpgrade(M0004.Upgrade, ctx, dbClient, &currentVersion, 4)
	execUpgrade(M0005.Upgrade, ctx, dbClient, &currentVersion, 5)
	execUpgrade(M0006.Upgrade, ctx, dbClient, &currentVersion, 6)
}

func Downgrade(ctx context.Context, dbClient *sql.DB) {
	currentVersion := getCurrentVersion(ctx, dbClient)

	execDowngrade(M0006.Downgrade, ctx, dbClient, &currentVersion, 5)
	execDowngrade(M0005.Downgrade, ctx, dbClient, &currentVersion, 4)
	execDowngrade(M0004.Downgrade, ctx, dbClient, &currentVersion, 3)
	execDowngrade(M0003.Downgrade, ctx, dbClient, &currentVersion, 2)
	execDowngrade(M0002.Downgrade, ctx, dbClient, &currentVersion, 1)
	execDowngrade(M0001.Downgrade, ctx, dbClient, &currentVersion, 0)
}

func execUpgrade(
	migration func(ctx context.Context, dbClient *sql.DB) error,
	ctx context.Context,
	dbClient *sql.DB,
	currentVersion *int8,
	aimedVersion int8,
) {
	if *currentVersion+1 == aimedVersion {
		err := migration(ctx, dbClient)
		if err != nil {
			log.Panicf("Migration failed: %s", err)
		}

		*currentVersion = aimedVersion
		updateVersion(ctx, dbClient, *currentVersion)
	}
}

func execDowngrade(
	migration func(ctx context.Context, dbClient *sql.DB) error,
	ctx context.Context,
	dbClient *sql.DB,
	currentVersion *int8,
	aimedVersion int8,
) {
	if *currentVersion-1 == aimedVersion {
		err := migration(ctx, dbClient)
		if err != nil {
			log.Panicf("Migration failed: %s", err)
		}

		*currentVersion = aimedVersion
		updateVersion(ctx, dbClient, *currentVersion)
	}
}

func getCurrentVersion(ctx context.Context, dbClient *sql.DB) int8 {
	var currentVersion int8
	row := dbClient.QueryRowContext(ctx, "SELECT version FROM migrations;")
	err := row.Scan(&currentVersion)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}

	return currentVersion
}

func updateVersion(ctx context.Context, dbClient *sql.DB, version int8) {
	_, err := dbClient.ExecContext(ctx, "DELETE FROM migrations; INSERT INTO migrations(version) values($1);", version)
	if err != nil {
		log.Panicf("Migration failed: %s", err)
	}
}
