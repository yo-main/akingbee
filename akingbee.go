package main

import (
	"akingbee/api"
	_ "akingbee/api"
	"akingbee/database"
	"akingbee/database/queries/migrations"
	"akingbee/database/repositories"
	"akingbee/models"
	"context"
	"log"

	"github.com/google/uuid"
)

func main() {
	// api.Serve()

	db, err := database.GetDb()

	if err != nil {
		log.Fatalf("Couldn't start database: %s", err)
	}

	ctx := context.TODO()

	migrations.Upgrade(ctx, db)

	email := "arnal.romain"
	user, err := repositories.GetUserByEmail(ctx, db, &email)

	if user == nil {

		new_user := models.User{
			PublicId: uuid.New(),
			Email:    "arnal.romain",
			Credentials: models.Credentials{
				PublicId: uuid.New(),
				Username: "romain",
				Password: "123",
			},
		}

		err = repositories.CreateCredentials(ctx, db, &new_user.Credentials)
		if err != nil {
			log.Fatalf("Couldn't create user: %s", err)
		}

		err = repositories.CreateUser(ctx, db, &new_user)
		if err != nil {
			log.Fatalf("Couldn't create user: %s", err)
		}

		user, err = repositories.GetUserByPublicId(ctx, db, &new_user.PublicId)

		if err != nil {
			log.Fatalf("Couldn't get user: %s", err)
		}
	}

	log.Printf("Retrieved user %s", user.Email)

	api.Serve()
}
