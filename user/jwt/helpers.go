package jwt

import (
	"akingbee/internal/config"
	"akingbee/user/models"
	"errors"
	"fmt"
	"github.com/golang-jwt/jwt"
	"github.com/google/uuid"
	"time"
)

func CreateToken(user *models.User) (string, error) {
	token := jwt.NewWithClaims(
		jwt.SigningMethodHS256,
		jwt.StandardClaims{
			Audience:  "all",
			ExpiresAt: time.Now().UTC().Add(time.Second * time.Duration(config.JWT_TTL)).Unix(),
			Issuer:    "akingbee",
			Subject:   user.PublicId.String(),
			Id:        "akingbee",
			IssuedAt:  time.Now().UTC().Unix(),
			NotBefore: time.Now().UTC().Unix(),
		},
	)
	jwt, err := token.SignedString(config.APP_PRIVATE_KEY)

	if err != nil {
		return "", err
	}
	return jwt, nil
}

func ValidateToken(tokenString string) (*uuid.UUID, error) {
	token, err := jwt.ParseWithClaims(tokenString, &jwt.StandardClaims{}, func(t *jwt.Token) (interface{}, error) { return config.APP_PRIVATE_KEY, nil })

	if err != nil {
		return nil, errors.New(fmt.Sprintf("JWT could not be parsed: %s", err))
	}

	claim := token.Claims.(*jwt.StandardClaims)

	err = claim.Valid()
	if err != nil {

		return nil, err
	}

	tk, err := uuid.Parse(claim.Subject)
	if err != nil {
		return nil, errors.New(fmt.Sprintf("Subject is not an UUID: %s", err))
	}

	return &tk, nil
}
