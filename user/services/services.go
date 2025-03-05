package services

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"

	"akingbee/auth/token"
	"akingbee/user/models"
	"akingbee/user/repositories"
)

type CreateUserCommand struct {
	Email    string
	Username string
	Password string
}

func HashPassword(password string) (string, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}

	return string(hashedPassword), nil
}

func CheckPasswordHash(password, hash string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
	return err == nil
}

var errNoEmail = errors.New("email has not been provided")
var errInvalidEmail = errors.New("email is not valid")
var errNoUsername = errors.New("username has not been provided")
var errInvalidUsername = errors.New("username is too short")
var errNoPassword = errors.New("password has not been provided")
var errInvalidPassword = errors.New("password should have at least 8 characters")
var errInvalidCredentials = errors.New("credentials are incorrect")

func (c *CreateUserCommand) Validate() error {
	if len(c.Email) == 0 {
		return errNoEmail
	}

	if len(c.Username) == 0 {
		return errNoUsername
	}

	if len(c.Password) == 0 {
		return errNoPassword
	}

	if len(c.Email) < 3 {
		return errInvalidEmail
	}

	if len(c.Username) < 3 {
		return errInvalidUsername
	}

	if len(c.Password) < 8 {
		return errInvalidPassword
	}

	return nil
}

func CreateUser(ctx context.Context, command *CreateUserCommand) (*models.User, error) {
	credentials := models.Credentials{
		PublicID: uuid.New(),
		Username: command.Username,
		Password: command.Password,
	}

	err := repositories.CreateCredentials(ctx, &credentials)
	if err != nil {
		log.Printf("Could not create credentials: %s", err)

		if strings.Contains(err.Error(), "UNIQUE constraint") {
			return nil, fmt.Errorf("email or username already taken: %w", err)
		}

		return nil, fmt.Errorf("couldn't create the user: %w", err)
	}

	user := models.User{
		PublicID:    uuid.New(),
		Email:       command.Email,
		Credentials: credentials,
	}
	err = repositories.CreateUser(ctx, &user)

	if err != nil {
		log.Printf("Could not create user: %s", err)
		return nil, fmt.Errorf("could not create user: %w", err)
	}

	return &user, nil
}

func LoginUser(password string, user *models.User) (string, error) {
	if !CheckPasswordHash(password, user.Credentials.Password) {
		log.Printf("Failed login for user %s (invalid password)", user.Credentials.Username)
		return "", errInvalidCredentials
	}

	token, err := token.CreateToken(user.PublicID.String(), user.IsAdmin())
	if err != nil {
		log.Printf("Could not generate jwt: %s", err)
		return "", fmt.Errorf("could not login with the user: %w", err)
	}

	return token, nil
}

func ImpersonateUser(ctx context.Context, impersonator *uuid.UUID, impersonatedUsername *uuid.UUID) (string, error) {
	user, err := repositories.GetUserByPublicID(ctx, impersonatedUsername)

	if err != nil {
		log.Printf("Could not get user by username with %s: %s", impersonatedUsername, err)
		return "", errInvalidCredentials
	}

	token, err := token.CreateTokenWithImpersonator(
		user.PublicID.String(),
		user.IsAdmin(),
		impersonator.String(),
	)
	if err != nil {
		log.Printf("Could not generate jwt: %s", err)
		return "", fmt.Errorf("could not login with the user: %w", err)
	}

	return token, nil
}

var errUserNotFound = errors.New("user not found")

func GetUser(ctx context.Context, userID *uuid.UUID) (*models.User, error) {
	user, err := repositories.GetUserByPublicID(ctx, userID)

	if err != nil {
		log.Printf("User could not be found: %s", err)
		return nil, errUserNotFound
	}

	return user, nil
}

var errUserNotAuthenticated = errors.New("user not authenticated")
var errIncorrectToken = errors.New("token is not a user token")

func AuthenticateUser(req *http.Request) (*models.AuthenticatedUser, error) {
	cookie, err := req.Cookie("akingbeeToken")

	if err != nil || len(cookie.Value) <= 2 {
		return nil, errUserNotAuthenticated
	}

	token, err := token.ValidateToken(cookie.Value)
	if err != nil {
		log.Printf("Invalid token: %s", err)
		return nil, errUserNotAuthenticated
	}

	userPublicID, err := uuid.Parse(token.Subject)
	if err != nil {
		log.Printf("Invalid token: %s", err)
		return nil, errIncorrectToken
	}

	var impersonatorPublicId *uuid.UUID

	if token.Impersonator != "" {
		publicID, err := uuid.Parse(token.Impersonator)
		if err != nil {
			log.Printf("Invalid token: %s", err)
			return nil, errIncorrectToken
		}

		impersonatorPublicId = &publicID
	}

	user, err := GetUser(req.Context(), &userPublicID)
	if err != nil {
		return nil, errUserNotFound
	}

	return &models.AuthenticatedUser{
		User:         user,
		Impersonator: impersonatorPublicId,
	}, nil
}
