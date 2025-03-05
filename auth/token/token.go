package token

import (
	"fmt"
	"time"

	"github.com/golang-jwt/jwt"

	"akingbee/internal/config"
)

type Token struct {
	Subject      string
	IsAdmin      bool
	Impersonator string
}

func signToken(claim Claim) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claim)
	jwt, err := token.SignedString(config.AppPrivateKey)

	if err != nil {
		return "", err
	}

	return jwt, nil
}

func getStandardClaim(subject string) jwt.StandardClaims {
	return jwt.StandardClaims{
		Audience:  "all",
		ExpiresAt: time.Now().UTC().Add(time.Second * time.Duration(config.TokenTTL)).Unix(),
		Issuer:    "akingbee",
		Subject:   subject,
		Id:        "akingbee",
		IssuedAt:  time.Now().UTC().Unix(),
		NotBefore: time.Now().UTC().Unix(),
	}
}

func CreateToken(subject string, isAdmin bool) (string, error) {
	token := Claim{
		StandardClaims: getStandardClaim(subject),
		IsAdmin:        isAdmin,
	}

	return signToken(token)
}

func CreateTokenWithImpersonator(subject string, isAdmin bool, impersonator string) (string, error) {
	token := Claim{
		StandardClaims: getStandardClaim(subject),
		IsAdmin:        isAdmin,
		Impersonator:   impersonator,
	}

	return signToken(token)
}

func ValidateToken(tokenString string) (*Token, error) {
	claim := Claim{}
	getKeyFunction := func(_ *jwt.Token) (interface{}, error) {
		return config.AppPrivateKey, nil
	}
	token, err := jwt.ParseWithClaims(tokenString, &claim, getKeyFunction)

	if err != nil {
		return nil, fmt.Errorf("JWT could not be parsed: %w", err)
	}

	err = token.Claims.Valid()
	if err != nil {
		return nil, err
	}

	return &Token{
		Subject:      claim.Subject,
		IsAdmin:      claim.IsAdmin,
		Impersonator: claim.Impersonator,
	}, nil
}
