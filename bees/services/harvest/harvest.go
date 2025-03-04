package harvest

import (
	"context"
	"time"

	"github.com/google/uuid"

	"akingbee/bees/models"
	"akingbee/bees/repositories"
)

type CreateHarvestCommand struct {
	Date         time.Time
	Quantity     int
	HivePublicID *uuid.UUID
}

func CreateHarvest(ctx context.Context, command *CreateHarvestCommand) (*models.Harvest, error) {
	harvest := models.Harvest{
		PublicID:     uuid.New(),
		Date:         command.Date,
		Quantity:     command.Quantity,
		HivePublicID: command.HivePublicID,
	}

	err := repositories.CreateHarvest(ctx, &harvest)

	if err != nil {
		return nil, err
	}

	return &harvest, nil
}
