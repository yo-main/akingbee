package user

import (
	"akingbee/user/jwt"
	"akingbee/user/models"
	"akingbee/user/repositories"
	"context"
	"errors"
	"log"
	"strings"

	"github.com/google/uuid"
)

type CreateUserCommand struct {
	Email    string
	Username string
	Password string
}

func (c *CreateUserCommand) Validate() error {
	if len(c.Email) == 0 {
		return errors.New("Email has not been provided")
	}
	if len(c.Username) == 0 {
		return errors.New("Username has not been provided")
	}
	if len(c.Password) == 0 {
		return errors.New("Password has not been provided")
	}
	if len(c.Email) < 3 {
		return errors.New("Email is not valid")
	}
	if len(c.Username) < 3 {
		return errors.New("Username is too short")
	}
	if len(c.Password) < 8 {
		return errors.New("Password should have at least 8 characters")
	}

	return nil
}

func CreateUser(ctx context.Context, command *CreateUserCommand) (*models.User, error) {
	credentials := models.Credentials{
		PublicId: uuid.New(),
		Username: command.Username,
		Password: command.Password,
	}

	err := repositories.CreateCredentials(ctx, &credentials)
	if err != nil {
		log.Printf("Could not create credentials: %s", err)
		if strings.Contains(err.Error(), "UNIQUE constraint") {
			return nil, errors.New("Email or Username already taken")
		}
		return nil, errors.New("Couldn't create the user")
	}

	user := models.User{
		PublicId:    uuid.New(),
		Email:       command.Email,
		Credentials: credentials,
	}
	err = repositories.CreateUser(ctx, &user)
	if err != nil {
		log.Printf("Could not create user: %s", err)
		return nil, err
	}

	return &user, nil
}

func LoginUser(ctx context.Context, username string, password string) (string, error) {
	user, err := repositories.GetUserByUsername(ctx, &username)

	if err != nil {
		log.Printf("Could not get user by username with %s: %s", username, err)
		return "", errors.New("Incorrect username or password")
	}

	token, err := jwt.CreateToken(user)
	if err != nil {
		log.Printf("Could not generate jwt: %s", err)
		return "", errors.New("Could not login in the user")
	}

	return token, nil
}
