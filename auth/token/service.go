package token

import (
	"fmt"
	"time"

	"github.com/golang-jwt/jwt"

	"akingbee/internal/config"
)

func signToken(claim Claim) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claim)
	jwt, err := token.SignedString(config.APP_PRIVATE_KEY)

	if err != nil {
		return "", err
	}

	return jwt, nil
}

func getStandardClaim(subject string) jwt.StandardClaims {
	return jwt.StandardClaims{
		Audience:  "all",
		ExpiresAt: time.Now().UTC().Add(time.Second * time.Duration(config.JWT_TTL)).Unix(),
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

func ValidateToken(tokenString string) (string, error) {
	claim := Claim{}
	getKeyFunction := func(_ *jwt.Token) (interface{}, error) {
		return config.APP_PRIVATE_KEY, nil
	}
	token, err := jwt.ParseWithClaims(tokenString, &claim, getKeyFunction)

	if err != nil {
		return "", fmt.Errorf("JWT could not be parsed: %w", err)
	}

	err = token.Claims.Valid()
	if err != nil {
		return "", err
	}

	return claim.Subject, nil
}
