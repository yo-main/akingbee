package main

import (
	"context"

	"akingbee/entrypoints"
	"akingbee/internal/database"
	"akingbee/internal/database/queries/migrations"
)

func main() {
	db := database.GetDB()
	ctx := context.Background()

	migrations.Upgrade(ctx, db)

	entrypoints.ApiServe()
}
