package repositories

import (
	"akingbee/bees/models"
	"akingbee/internal/database"
	"context"
	"fmt"
	"log"

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
	db := database.GetDB()

	_, err := db.ExecContext(
		ctx,
		queryCreateComment,
		comment.PublicID,
		comment.Date,
		comment.Type,
		comment.Body,
		comment.HivePublicID,
	)

	return err
}

const queryGetComment = `
	SELECT 
		COMMENT.PUBLIC_ID,
		DATE,
		TYPE,
		BODY,
		HIVE.PUBLIC_ID
	FROM COMMENT
	JOIN HIVE ON COMMENT.HIVE_ID=HIVE.ID
`

func GetComment(ctx context.Context, commentPublicID *uuid.UUID) (*models.Comment, error) {
	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryGetComment+" WHERE COMMENT.PUBLIC_ID=$1", commentPublicID)

	if err != nil {
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

	var comment models.Comment

	for rows.Next() {
		err := rows.Scan(
			&comment.PublicID,
			&comment.Date,
			&comment.Type,
			&comment.Body,
			&comment.HivePublicID,
		)
		if err != nil {
			return nil, fmt.Errorf("could not build Comment from result: %w", err)
		}
	}

	if rows.Err() != nil {
		return nil, fmt.Errorf("rows closed unexpectedly: %w", rows.Err())
	}

	return &comment, nil
}

func GetComments(ctx context.Context, hivePublicID *uuid.UUID) ([]models.Comment, error) {
	db := database.GetDB()
	query := queryGetComment + " WHERE HIVE.PUBLIC_ID=$1 ORDER BY COMMENT.DATE_CREATION DESC"
	rows, err := db.QueryContext(ctx, query, hivePublicID)

	if err != nil {
		log.Printf("%s", err)
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

	var comments []models.Comment

	for rows.Next() {
		var comment models.Comment
		err := rows.Scan(
			&comment.PublicID,
			&comment.Date,
			&comment.Type,
			&comment.Body,
			&comment.HivePublicID,
		)

		if err != nil {
			return nil, fmt.Errorf("could not build Comment from result: %w", err)
		}

		comments = append(comments, comment)
	}

	if rows.Err() != nil {
		return nil, fmt.Errorf("rows closed unexpectedly: %w", rows.Err())
	}

	return comments, nil
}

const queryUpdateComment = `
	UPDATE COMMENT 
	SET DATE=$1, TYPE=$2, BODY=$3
	WHERE PUBLIC_ID=$4
`

func UpdateComment(ctx context.Context, comment *models.Comment) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryUpdateComment, comment.Date, comment.Type, comment.Body, comment.PublicID)

	return err
}

const queryDeleteComment = `
	DELETE FROM COMMENT 
	WHERE PUBLIC_ID=$1
`

func DeleteComment(ctx context.Context, comment *models.Comment) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryDeleteComment, comment.PublicID)

	return err
}
