package apiary

import (
	"context"
	"errors"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/bees/repositories"
)

type CreateApiaryCommand struct {
	Name      string
	Location  string
	HoneyKind string
	User      *uuid.UUID
}

var errNameNotProvided = errors.New("name has not been provided")
var errLocationNotProvided = errors.New("location has not been provided")
var errHoneyKindNotProvided = errors.New("honeyKind has not been provided")
var errUserNotProvided = errors.New("user has not been provided")

func (c *CreateApiaryCommand) Validate() error {
	if len(c.Name) == 0 {
		return errNameNotProvided
	}

	if len(c.Location) == 0 {
		return errLocationNotProvided
	}

	if len(c.HoneyKind) == 0 {
		return errHoneyKindNotProvided
	}

	if c.User == nil {
		return errUserNotProvided
	}

	return nil
}

type UpdateApiaryCommand struct {
	Name      string
	Location  string
	HoneyKind string
	User      *uuid.UUID
	PublicID  *uuid.UUID
}

func (c *UpdateApiaryCommand) Validate() error {
	if len(c.Name) == 0 {
		return errNameNotProvided
	}

	if len(c.Location) == 0 {
		return errLocationNotProvided
	}

	if len(c.HoneyKind) == 0 {
		return errHoneyKindNotProvided
	}

	return nil
}

func CreateApiary(ctx context.Context, command *CreateApiaryCommand) (*models.Apiary, error) {
	err := command.Validate()
	if err != nil {
		return nil, err
	}

	apiary := models.Apiary{
		HoneyKind: command.HoneyKind,
		Name:      command.Name,
		Location:  command.Location,
		User:      *command.User,
		HiveCount: 0,
		PublicID:  uuid.New(),
	}

	err = repositories.CreateApiary(ctx, &apiary)
	if err != nil {
		log.Printf("Could not create apiary: %s", err)
		return nil, fmt.Errorf("couldn't create the apiary: %w", err)
	}

	return &apiary, nil
}

func UpdateApiary(ctx context.Context, apiary *models.Apiary) error {
	err := repositories.UpdateApiary(ctx, apiary)
	if err != nil {
		log.Printf("Could not update apiary: %s", err)
		return fmt.Errorf("couldn't update the apiary: %w", err)
	}

	return nil
}

func DeleteApiary(ctx context.Context, apiary *models.Apiary) error {
	err := repositories.DeleteApiary(ctx, apiary)
	if err != nil {
		log.Printf("Could not delete apiary: %s", err)
		return fmt.Errorf("couldn't delete the apiary: %w", err)
	}

	return nil
}
