package migrations

import (
	"akingbee/internal/database/queries/migrations/M0001"
	"akingbee/internal/database/queries/migrations/M0002"
	"context"
	"database/sql"
)

func Upgrade(ctx context.Context, db *sql.DB) {
	M0001.Upgrade(ctx, db)
	M0002.Upgrade(ctx, db)
}

func Downgrade(ctx context.Context, db *sql.DB) {
	M0002.Downgrade(ctx, db)
	M0001.Downgrade(ctx, db)
}
