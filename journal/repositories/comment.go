package repositories

import (
	"context"
	"fmt"
	"log"

	"github.com/google/uuid"

	"akingbee/internal/database"
	"akingbee/journal/models"
)

const queryCreateComment = `
	INSERT INTO COMMENT (
		public_id, date, type, body, hive_id, apiary_id
	) VALUES (
		$1, 
		$2,
		$3,
		$4,
		(SELECT HIVE.ID FROM HIVE WHERE HIVE.PUBLIC_ID=$5),
		(SELECT APIARY.ID FROM APIARY WHERE APIARY.PUBLIC_ID=$6)
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
		comment.ApiaryPublicID,
	)

	return err
}

const queryGetComment = `
	SELECT 
		COMMENT.PUBLIC_ID,
		DATE,
		TYPE,
		BODY,
		HIVE.PUBLIC_ID AS HIVE_PUBLIC_ID,
		APIARY.PUBLIC_ID AS APIARY_PUBLIC_ID
	FROM COMMENT
	LEFT JOIN HIVE ON COMMENT.HIVE_ID=HIVE.ID
	LEFT JOIN APIARY ON COMMENT.APIARY_ID=APIARY.ID
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
			&comment.ApiaryPublicID,
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
			&comment.ApiaryPublicID,
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

const queryListApiariesWithComment = `
	WITH MOST_RECENT_COMMENT AS (
		SELECT
			APIARY_ID,
			MAX(ID) OVER(ORDER BY DATE_CREATION) AS ID
		FROM COMMENT
		GROUP BY APIARY_ID
	)
	SELECT 
		APIARY.PUBLIC_ID AS APIARY_PUBLIC_ID,
		APIARY.NAME AS APIARY_NAME,
		USERS.PUBLIC_ID AS USER_PUBLIC_ID, 
		COMMENT.PUBLIC_ID AS COMMENT_PUBLIC_ID,
		COALESCE(COMMENT.BODY, '') AS COMMENT_BODY,
		COMMENT.DATE AS COMMENT_DATE,
		COALESCE(COMMENT.TYPE, '') AS COMMENT_TYPE
	FROM APIARY
	JOIN USERS ON USERS.ID=APIARY.USER_ID
	LEFT JOIN MOST_RECENT_COMMENT ON APIARY.ID=MOST_RECENT_COMMENT.APIARY_ID
	LEFT JOIN COMMENT ON COMMENT.ID=MOST_RECENT_COMMENT.ID
	WHERE USERS.PUBLIC_ID = $1
`

func ListApiariesWithComment(ctx context.Context, userPublicId *uuid.UUID) ([]models.ApiaryWithComment, error) {
	db := database.GetDB()
	rows, err := db.QueryContext(ctx, queryListApiariesWithComment, userPublicId)

	if err != nil {
		return nil, fmt.Errorf("error executing query: %w", err)
	}

	defer database.CloseRows(rows)

	var comments []models.ApiaryWithComment

	for rows.Next() {
		var comment models.ApiaryWithComment

		err := rows.Scan(
			&comment.ApiaryPublicID,
			&comment.ApiaryName,
			&comment.ApiaryUser,
			&comment.CommentPublicId,
			&comment.CommentBody,
			&comment.CommentDate,
			&comment.CommentType,
		)
		if err != nil {
			return nil, fmt.Errorf("could not build ApiaryWithComment from result: %w", err)
		}

		comments = append(comments, comment)
	}

	if rows.Err() != nil {
		return nil, fmt.Errorf("rows closed unexpectedly: %w", rows.Err())
	}

	return comments, nil
}
