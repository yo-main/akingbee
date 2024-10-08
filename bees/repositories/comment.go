package repositories

import (
	"akingbee/bees/models"
	"akingbee/internal/database"
	"context"
	"errors"
	"fmt"
	"github.com/google/uuid"
)

const queryCreateComment = `
	INSERT INTO COMMENT (
		public_id, date, type, body, hive_id
	) VALUES (
		$1, 
		$2,
		$3,
		$4,
		(SELECT HIVE.ID FROM HIVE WHERE HIVE.PUBLIC_ID=$5)
	)
`

func CreateComment(ctx context.Context, comment *models.Comment) error {
	db := database.GetDb()

	_, err := db.ExecContext(
		ctx,
		queryCreateSwarm,
		comment.PublicId,
		comment.Date,
		comment.Type,
		comment.Body,
		comment.HivePublicId,
	)

	return err
}

const queryGetComment = `
	SELECT 
		PUBLIC_ID,
		DATE,
		TYPE,
		BODY,
		HIVE.PUBLIC_ID
	FROM COMMENT
	JOIN HIVE ON COMMENT.HIVE_ID=HIVE.ID
	WHERE PUBLIC_ID=$1
`

func GetComment(ctx context.Context, commentPublicId *uuid.UUID) (*models.Comment, error) {
	db := database.GetDb()
	rows, err := db.QueryContext(ctx, queryGetComment, commentPublicId)
	defer rows.Close()

	if err != nil {
		return nil, errors.New(fmt.Sprintf("Error executing query: %s", err))
	}

	var comment models.Comment

	for rows.Next() {
		err := rows.Scan(
			&comment.PublicId,
			&comment.Date,
			&comment.Type,
			&comment.Body,
			&comment.HivePublicId,
		)
		if err != nil {
			return nil, errors.New(fmt.Sprintf("Could not build Comment from result: %s", err))
		}
	}

	return &comment, nil
}

const queryUpdateComment = `
	UPDATE COMMENT 
	SET DATE=$1, TYPE=$2, BODY=$3
	WHERE PUBLIC_ID=$4
`

func UpdateComment(ctx context.Context, comment *models.Comment) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryUpdateSwarm, comment.Date, comment.Type, comment.Body, comment.PublicId)
	return err
}

const queryDeleteComment = `
	DELETE FROM COMMENT 
	WHERE PUBLIC_ID=$1
`

func DeleteComment(ctx context.Context, comment *models.Comment) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, queryDeleteSwarm, comment.PublicId)
	return err
}
