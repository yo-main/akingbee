package token

import (
	"github.com/golang-jwt/jwt"
)

type Claim struct {
	jwt.StandardClaims
	IsAdmin      bool   `json:"adm,omitempty"`
	Impersonator string `json:"imp,omitempty"`
}

func (c Claim) Valid() error {
	return c.StandardClaims.Valid()
}
