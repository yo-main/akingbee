package main

import (
	"akingbee/app/core/database"
	"akingbee/app/core/database/queries/migrations"
	"akingbee/app/entrypoints"
	"context"
)

func main() {
	// api.Serve()

	db := database.GetDb()
	ctx := context.TODO()

	migrations.Upgrade(ctx, db)

	// email := "arnal.romain"
	// user, err := repositories.GetUserByEmail(ctx, db, &email)

	// if user == nil {

	// 	new_user := models.User{
	// 		PublicId: uuid.New(),
	// 		Email:    "arnal.romain",
	// 		Credentials: models.Credentials{
	// 			PublicId: uuid.New(),
	// 			Username: "romain",
	// 			Password: "123",
	// 		},
	// 	}

	// 	err = repositories.CreateCredentials(ctx, db, &new_user.Credentials)
	// 	if err != nil {
	// 		log.Fatalf("Couldn't create user: %s", err)
	// 	}

	// 	err = repositories.CreateUser(ctx, db, &new_user)
	// 	if err != nil {
	// 		log.Fatalf("Couldn't create user: %s", err)
	// 	}

	// 	user, err = repositories.GetUserByPublicId(ctx, db, &new_user.PublicId)

	// 	if err != nil {
	// 		log.Fatalf("Couldn't get user: %s", err)
	// 	}
	// }

	// log.Printf("Retrieved user %s", user.Email)

	entrypoints.ApiServe()
}
