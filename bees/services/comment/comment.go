package comment

import (
	"akingbee/bees/models"
	"akingbee/bees/repositories"
	"context"
	"errors"
	"log"
	"time"

	"github.com/google/uuid"
)

type CreateCommentCommand struct {
	Date         time.Time
	Type         string
	Body         string
	HivePublicID uuid.UUID
	User         *uuid.UUID
}

func (c *CreateCommentCommand) Validate() error {
	if len(c.Type) == 0 {
		return errors.New("Comment type has not been provided")
	}
	if c.Body == "" {
		return errors.New("Comment body has not been provided")
	}

	return nil
}

func CreateComment(ctx context.Context, command *CreateCommentCommand) (*models.Comment, error) {
	err := command.Validate()
	if err != nil {
		return nil, err
	}

	comment := models.Comment{
		Date:         command.Date,
		Type:         command.Type,
		Body:         command.Body,
		HivePublicID: &command.HivePublicID,
		PublicID:     uuid.New(),
	}

	err = repositories.CreateComment(ctx, &comment)
	if err != nil {
		log.Printf("Could not create comment: %s", err)
		return nil, errors.New("Couldn't create the comment")
	}

	return &comment, nil
}

func UpdateComment(ctx context.Context, comment *models.Comment) error {
	err := repositories.UpdateComment(ctx, comment)
	if err != nil {
		log.Printf("Could not update comment: %s", err)
		return errors.New("Couldn't update the comment")
	}

	return nil
}

func DeleteComment(ctx context.Context, comment *models.Comment) error {
	err := repositories.DeleteComment(ctx, comment)
	if err != nil {
		log.Printf("Could not delete comment: %s", err)
		return errors.New("Couldn't delete the comment")
	}

	return nil
}
