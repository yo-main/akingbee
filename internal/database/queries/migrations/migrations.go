package migrations

import (
	"akingbee/internal/database/queries/migrations/M0001"
	"akingbee/internal/database/queries/migrations/M0002"
	"context"
	"database/sql"
	"fmt"
	"log"
)

func Upgrade(ctx context.Context, db *sql.DB) {
	log.Print("Running migrations")

	err := M0001.Upgrade(ctx, db)
	if err != nil {
		log.Printf(fmt.Sprintf("Migration failed: %s", err))
		return
	}

	err = M0002.Upgrade(ctx, db)
	if err != nil {
		log.Printf(fmt.Sprintf("Migration failed: %s", err))
		return
	}
}

func Downgrade(ctx context.Context, db *sql.DB) {
	M0002.Downgrade(ctx, db)
	M0001.Downgrade(ctx, db)
}
