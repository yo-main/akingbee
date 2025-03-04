package repositories

import (
	"akingbee/internal/database"
	"akingbee/user/models"
	"context"

	"github.com/google/uuid"
)

const queryCreateCredentials = `
	INSERT INTO CREDENTIALS (
		public_id, username, password
	) VALUES (
		$1, $2, $3
	)
`

func CreateCredentials(ctx context.Context, credentials *models.Credentials) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryCreateCredentials, credentials.PublicID, credentials.Username, credentials.Password)

	return err
}

const queryCreateUser = `
	INSERT INTO USERS (
		public_id, email, credential_id
	) VALUES (
		$1, $2, (SELECT ID FROM CREDENTIALS WHERE CREDENTIALS.PUBLIC_ID=$3)
	)
`

func CreateUser(ctx context.Context, user *models.User) error {
	db := database.GetDB()
	_, err := db.ExecContext(ctx, queryCreateUser, user.PublicID, user.Email, user.Credentials.PublicID)

	return err
}

const queryGetUser = `
	SELECT USERS.public_id, USERS.email, CREDENTIALS.public_id, CREDENTIALS.username, CREDENTIALS.password
	FROM USERS
	JOIN CREDENTIALS ON USERS.CREDENTIAL_ID=CREDENTIALS.ID
`

func getUser(ctx context.Context, query string, params interface{}) (*models.User, error) {
	db := database.GetDB()
	row := db.QueryRowContext(ctx, query, params)

	var user models.User
	var credentials models.Credentials

	err := row.Scan(&user.PublicID, &user.Email, &credentials.PublicID, &credentials.Username, &credentials.Password)

	if err != nil {
		return nil, err
	}

	user.Credentials = credentials

	return &user, nil
}

func getUsers(ctx context.Context, query string) ([]*models.User, error) {
	db := database.GetDB()
	rows, err := db.QueryContext(ctx, query)

	if err != nil {
		return nil, err
	}

	var users []*models.User

	for rows.Next() {
		var user models.User
		var credentials models.Credentials

		err := rows.Scan(&user.PublicID, &user.Email, &credentials.PublicID, &credentials.Username, &credentials.Password)
		if err != nil {
			return nil, err
		}

		user.Credentials = credentials
		users = append(users, &user)
	}

	return users, nil
}

func GetUserByPublicID(ctx context.Context, publicID *uuid.UUID) (*models.User, error) {
	query := queryGetUser + " WHERE USERS.public_id=$1"
	return getUser(ctx, query, publicID)
}

func GetUserByEmail(ctx context.Context, email *string) (*models.User, error) {
	query := queryGetUser + " WHERE USERS.email=$1"
	return getUser(ctx, query, email)
}

func GetUserByUsername(ctx context.Context, username *string) (*models.User, error) {
	query := queryGetUser + " WHERE CREDENTIALS.username=$1"
	return getUser(ctx, query, username)
}

func ListUsers(ctx context.Context) ([]*models.User, error) {
	query := queryGetUser
	return getUsers(ctx, query)
}
