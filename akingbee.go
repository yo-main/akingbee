package main

import (
	"akingbee/entrypoints"
	"akingbee/internal/database"
	"akingbee/internal/database/queries/migrations"
	"context"
)

func main() {
	// api.Serve()

	db := database.GetDb()
	ctx := context.TODO()

	migrations.Upgrade(ctx, db)

	entrypoints.ApiServe()
}
