package apiary

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"
	"context"
	"errors"
	"github.com/google/uuid"
	"log"
)

type CreateApiaryCommand struct {
	Name      string
	Location  string
	HoneyKind string
	Owner     *uuid.UUID
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

	if c.Owner == nil {
		return errors.New("Owner has not been provided")
	}

	return nil
}

type UpdateApiaryCommand struct {
	Name      string
	Location  string
	HoneyKind string
	Owner     *uuid.UUID
	PublicId  *uuid.UUID
}

func (c *UpdateApiaryCommand) Validate() error {
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
	err := command.Validate()
	if err != nil {
		return nil, err
	}

	apiary := models.Apiary{
		HoneyKind: command.HoneyKind,
		Name:      command.Name,
		Location:  command.Location,
		Owner:     *command.Owner,
		HiveCount: 0,
		PublicId:  uuid.New(),
	}

	err = repositories.CreateApiary(ctx, &apiary)
	if err != nil {
		log.Printf("Could not create apiary: %s", err)
		return nil, errors.New("Couldn't create the apiary")
	}

	return &apiary, nil
}

func UpdateApiary(ctx context.Context, apiary *models.Apiary) error {
	err := repositories.UpdateApiary(ctx, apiary)
	if err != nil {
		log.Printf("Could not update apiary: %s", err)
		return errors.New("Couldn't update the apiary")
	}

	return nil
}

func DeleteApiary(ctx context.Context, apiary *models.Apiary) error {
	err := repositories.DeleteApiary(ctx, apiary)
	if err != nil {
		log.Printf("Could not delete apiary: %s", err)
		return errors.New("Couldn't delete the apiary")
	}

	return nil
}
