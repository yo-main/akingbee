package main

import (
	_ "akingbee/api"
	"akingbee/database"
	"akingbee/database/queries/migrations"
	"akingbee/database/repositories"
	"akingbee/models"
	"context"
	"github.com/google/uuid"
	"log"
)

func main() {
	// api.Serve()

	db, err := database.GetDb()

	if err != nil {
		log.Fatalf("Couldn't start database: %s", err)
	}

	ctx := context.TODO()

	migrations.Upgrade(ctx, db)

	user := models.User{
		PublicId: uuid.New(),
		Email:    "arnal.romain",
		Credentials: models.Credentials{
			PublicId: uuid.New(),
			Username: "romain",
			Password: "123",
		},
	}

	err = repositories.CreateCredentials(ctx, db, &user.Credentials)
	if err != nil {
		log.Fatalf("Couldn't create user: %s", err)
	}

	err = repositories.CreateUser(ctx, db, &user)
	if err != nil {
		log.Fatalf("Couldn't create user: %s", err)
	}

	db_user, err := repositories.GetUser(ctx, db, &user.PublicId)

	if err != nil {
		log.Fatalf("Couldn't get user: %s", err)
	}

	log.Printf("Retrieved user %s from %s", db_user.PublicId, user.PublicId)

}
