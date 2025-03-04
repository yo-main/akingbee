package jwt

import (
	"fmt"
	"strings"
	"time"

	"github.com/golang-jwt/jwt"
	"github.com/google/uuid"

	"akingbee/internal/config"
)

func CreateToken(subject string) (string, error) {
	token := jwt.NewWithClaims(
		jwt.SigningMethodHS256,
		jwt.StandardClaims{
			Audience:  "all",
			ExpiresAt: time.Now().UTC().Add(time.Second * time.Duration(config.JWT_TTL)).Unix(),
			Issuer:    "akingbee",
			Subject:   subject,
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
		return nil, fmt.Errorf("JWT could not be parsed: %s", err)
	}

	claim := token.Claims.(*jwt.StandardClaims)

	err = claim.Valid()
	if err != nil {
		return nil, err
	}

	return parseSubject(claim.Subject)
}

func parseSubject(subject string) (*uuid.UUID, error) {
	parts := strings.Split(subject, ":")
	userToken := parts[len(parts)-1]

	tk, err := uuid.Parse(userToken)
	if err != nil {
		return nil, fmt.Errorf("Subject is not an UUID: %s", err)
	}

	return &tk, nil
}
