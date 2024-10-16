package harvest

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"
	"context"
	"time"

	"github.com/google/uuid"
)

type CreateHarvestCommand struct {
	Date         time.Time
	Quantity     int
	HivePublicId *uuid.UUID
}

func CreateHarvest(ctx context.Context, command *CreateHarvestCommand) (*models.Harvest, error) {
	harvest := models.Harvest{
		PublicId:     uuid.New(),
		Date:         command.Date,
		Quantity:     command.Quantity,
		HivePublicId: command.HivePublicId,
	}

	err := repositories.CreateHarvest(ctx, &harvest)

	if err != nil {
		return nil, err
	}

	return &harvest, nil
}
