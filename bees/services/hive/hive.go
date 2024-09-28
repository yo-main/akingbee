package hive

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"
	"context"
	"errors"
	"github.com/google/uuid"
	"log"
)

type CreateHiveCommand struct {
	Name      string
	Condition string
	Owner     *uuid.UUID
}

func (c *CreateHiveCommand) Validate() error {
	if len(c.Name) == 0 {
		return errors.New("Name has not been provided")
	}
	if len(c.Condition) == 0 {
		return errors.New("Condition has not been provided")
	}
	if c.Owner == nil {
		return errors.New("Owner has not been provided")
	}

	return nil
}

type UpdateHiveCommand struct {
	Name      string
	Condition string
	Owner     *uuid.UUID
	PublicId  *uuid.UUID
}

func (c *UpdateHiveCommand) Validate() error {
	if len(c.Name) == 0 {
		return errors.New("Name has not been provided")
	}
	if len(c.Condition) == 0 {
		return errors.New("Location has not been provided")
	}
	return nil
}

func CreateHive(ctx context.Context, command *CreateHiveCommand) (*models.Hive, error) {
	err := command.Validate()
	if err != nil {
		return nil, err
	}

	hive := models.Hive{
		Name:      command.Name,
		Condition: command.Condition,
		Owner:     *command.Owner,
		PublicId:  uuid.New(),
	}

	err = repositories.CreateHive(ctx, &hive)
	if err != nil {
		log.Printf("Could not create hive: %s", err)
		return nil, errors.New("Couldn't create the hive")
	}

	return &hive, nil
}

func UpdateHive(ctx context.Context, hive *models.Hive) error {
	err := repositories.UpdateHive(ctx, hive)
	if err != nil {
		log.Printf("Could not update hive: %s", err)
		return errors.New("Couldn't update the hive")
	}

	return nil
}

func DeleteHive(ctx context.Context, hive *models.Hive) error {
	err := repositories.DeleteHive(ctx, hive)
	if err != nil {
		log.Printf("Could not delete hive: %s", err)
		return errors.New("Couldn't delete the hive")
	}

	return nil
}
