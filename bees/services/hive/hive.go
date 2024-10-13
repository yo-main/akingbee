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
	Name        string
	Beekeeper   string
	Apiary      *uuid.UUID
	SwarmHealth string
	User        *uuid.UUID
}

func (c *CreateHiveCommand) Validate() error {
	if len(c.Name) == 0 {
		return errors.New("Name has not been provided")
	}
	if len(c.Beekeeper) == 0 {
		return errors.New("Beekeeper has not been provided")
	}
	if c.User == nil {
		return errors.New("User has not been provided")
	}

	return nil
}

type UpdateHiveCommand struct {
	Name      string
	Beekeeper string
	User      *uuid.UUID
	PublicId  *uuid.UUID
}

func (c *UpdateHiveCommand) Validate() error {
	if len(c.Name) == 0 {
		return errors.New("Name has not been provided")
	}
	if len(c.Beekeeper) == 0 {
		return errors.New("Beekeeper has not been provided")
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
		Beekeeper: command.Beekeeper,
		User:      *command.User,
		PublicId:  uuid.New(),
	}

	if command.Apiary != nil {
		apiary, err := repositories.GetApiary(ctx, command.Apiary)
		if err != nil {
			log.Printf("Could not find apiary %s", command.Apiary)
			return nil, errors.New("Could not find Apiary")
		}

		if apiary.User != *command.User {
			log.Printf("Forbidden: apiary %s does not belong to current user %s", command.Apiary, command.User)
			return nil, errors.New("Forbidden access")
		}

		hive.SetApiary(apiary)
	}

	if command.SwarmHealth != "" {
		swarm := models.NewSwarm(command.SwarmHealth)
		err := repositories.CreateSwarm(ctx, swarm)
		if err != nil {
			log.Printf("Could not create swarm %s", err)
			return nil, errors.New("Could not create swarm")
		}

		hive.SetSwarm(swarm)
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

	if hive.GetSwarm() != nil {
		repositories.UpdateSwarm(ctx, hive.GetSwarm())
	}

	if hive.GetApiary() != nil {
		repositories.UpdateApiary(ctx, hive.GetApiary())
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
