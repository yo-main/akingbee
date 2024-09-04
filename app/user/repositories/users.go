package repositories

import (
	"akingbee/app/core/database"
	"akingbee/app/user/models"
	"context"

	"github.com/google/uuid"
)

const createCredentials = `
	INSERT INTO CREDENTIALS (
		public_id, username, password
	) VALUES (
		$1, $2, $3
	)
`

func CreateCredentials(ctx context.Context, credentials *models.Credentials) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, createCredentials, credentials.PublicId, credentials.Username, credentials.Password)
	return err
}

const createUser = `
	INSERT INTO USERS (
		public_id, email, credential_id
	) VALUES (
		$1, $2, (SELECT ID FROM CREDENTIALS WHERE CREDENTIALS.PUBLIC_ID=$3)
	)
`

func CreateUser(ctx context.Context, user *models.User) error {
	db := database.GetDb()
	_, err := db.ExecContext(ctx, createUser, user.PublicId, user.Email, user.Credentials.PublicId)
	return err
}

const getUser = `
	SELECT USERS.public_id, USERS.email, CREDENTIALS.public_id, CREDENTIALS.username, CREDENTIALS.password
	FROM USERS
	JOIN CREDENTIALS ON USERS.CREDENTIAL_ID=CREDENTIALS.ID
`

func GetUser(ctx context.Context, query string, params interface{}) (*models.User, error) {
	db := database.GetDb()
	row := db.QueryRowContext(ctx, query, params)

	var user models.User
	var credentials models.Credentials

	err := row.Scan(&user.PublicId, &user.Email, &credentials.PublicId, &credentials.Username, &credentials.Password)

	if err != nil {
		return nil, err
	}

	return &user, nil
}

func GetUserByPublicId(ctx context.Context, publicId *uuid.UUID) (*models.User, error) {
	query := getUser + " WHERE USERS.public_id=$1"
	return GetUser(ctx, query, publicId)
}

func GetUserByEmail(ctx context.Context, email *string) (*models.User, error) {
	query := getUser + " WHERE USERS.email=$1"
	return GetUser(ctx, query, email)
}
