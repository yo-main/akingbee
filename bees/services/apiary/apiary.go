package apiary

import (
	"akingbee/bees/models"
	"context"
	"errors"
	"github.com/google/uuid"
)

type CreateApiaryCommand struct {
	Name      string
	Location  string
	HoneyKind string
}

func (c *CreateApiaryCommand) Validate() error {
	if len(c.Name) == 0 {
		return errors.New("Name has not been provided")
	}
	if len(c.Location) == 0 {
		return errors.New("Location has not been provided")
	}
	if len(c.HoneyKind) == 0 {
		return errors.New("HoneyKind has not been provided")
	}

	return nil
}

func CreateApiary(ctx context.Context, command *CreateApiaryCommand) (*models.Apiary, error) {
	apiary := models.Apiary{
		HoneyKind: command.HoneyKind,
		Name:      command.Name,
		Location:  command.Location,
		PublicId:  uuid.New(),
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
