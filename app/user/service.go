package user

import (
	"akingbee/app/user/models"
	"akingbee/app/user/repositories"
	"context"
	"log"

	"github.com/google/uuid"
)

func CreateUser(ctx context.Context, email string, username string, password string) (*models.User, error) {
	credentials := models.Credentials{
		PublicId: uuid.New(),
		Username: username,
		Password: password,
	}

	err := repositories.CreateCredentials(ctx, &credentials)
	if err != nil {
		log.Printf("Could not create credentials: %s", err)
		return nil, err
	}

	user := models.User{
		PublicId:    uuid.New(),
		Email:       email,
		Credentials: credentials,
	}
	err = repositories.CreateUser(ctx, &user)
	if err != nil {
		log.Printf("Could not create user: %s", err)
		return nil, err
	}

	return &user, nil
}
