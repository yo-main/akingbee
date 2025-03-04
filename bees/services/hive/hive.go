package hive

import (
	"context"
	"errors"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/bees/repositories"
)

type CreateHiveCommand struct {
	Name        string
	Beekeeper   string
	Apiary      *uuid.UUID
	SwarmHealth string
	User        *uuid.UUID
}

var errNameNotProvided = errors.New("name has not been provided")
var errBeekeeperNotProvided = errors.New("beekeeper has not been provided")
var errUserNotProvided = errors.New("user has not been provided")
var errApiaryNotFound = errors.New("apiary not found")
var errForbiddenAccess = errors.New("forbidden access")

func (c *CreateHiveCommand) Validate() error {
	if len(c.Name) == 0 {
		return errNameNotProvided
	}

	if len(c.Beekeeper) == 0 {
		return errBeekeeperNotProvided
	}

	if c.User == nil {
		return errUserNotProvided
	}

	return nil
}

type UpdateHiveCommand struct {
	Name      string
	Beekeeper string
	User      *uuid.UUID
	PublicID  *uuid.UUID
}

func (c *UpdateHiveCommand) Validate() error {
	if len(c.Name) == 0 {
		return errNameNotProvided
	}

	if len(c.Beekeeper) == 0 {
		return errBeekeeperNotProvided
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
		PublicID:  uuid.New(),
	}

	if command.Apiary != nil {
		apiary, err := repositories.GetApiary(ctx, command.Apiary)
		if err != nil {
			log.Printf("Could not find apiary %s", command.Apiary)
			return nil, errApiaryNotFound
		}

		if apiary.User != *command.User {
			log.Printf("Forbidden: apiary %s does not belong to current user %s", command.Apiary, command.User)
			return nil, errForbiddenAccess
		}

		hive.SetApiary(apiary)
	}

	if command.SwarmHealth != "" {
		swarm := models.NewSwarm(command.SwarmHealth)
		err := repositories.CreateSwarm(ctx, swarm)

		if err != nil {
			log.Printf("Could not create swarm %s", err)
			return nil, fmt.Errorf("could not create swarm: %w", err)
		}

		hive.SetSwarm(swarm)
	}

	err = repositories.CreateHive(ctx, &hive)
	if err != nil {
		log.Printf("Could not create hive: %s", err)
		return nil, fmt.Errorf("could not create hive: %w", err)
	}

	return &hive, nil
}

func UpdateHive(ctx context.Context, hive *models.Hive) error {
	err := repositories.UpdateHive(ctx, hive)
	if err != nil {
		log.Printf("Could not update hive: %s", err)
		return fmt.Errorf("could not update hive: %w", err)
	}

	if hive.GetSwarm() != nil {
		err = repositories.UpdateSwarm(ctx, hive.GetSwarm())

		if err != nil {
			log.Printf("Could not update swarm: %s", err)
			return fmt.Errorf("could not update swarm: %w", err)
		}
	}

	if hive.GetApiary() != nil {
		err = repositories.UpdateApiary(ctx, hive.GetApiary())

		if err != nil {
			log.Printf("Could not update apiary: %s", err)
			return fmt.Errorf("could not update apiary: %w", err)
		}
	}

	return nil
}

func DeleteHive(ctx context.Context, hive *models.Hive) error {
	err := repositories.DeleteHive(ctx, hive)
	if err != nil {
		log.Printf("Could not delete hive: %s", err)
		return fmt.Errorf("could not delete hive: %w", err)
	}

	return nil
}
