package jwt

import (
	"akingbee/internal/config"
	"akingbee/user/models"
	"crypto"
	"time"

	"github.com/golang-jwt/jwt"
)

func CreateToken(user *models.User) (string, error) {
	token := jwt.NewWithClaims(
		&jwt.SigningMethodHMAC{
			Name: "IDK",
			Hash: crypto.SHA256,
		},
		jwt.MapClaims{
			"iss": "akingbee",
			"sub": user.PublicId,
			"exp": time.Now().UTC().Add(time.Second * time.Duration(config.JWT_TTL)).Unix(),
		},
	)
	jwt, err := token.SignedString(config.APP_PRIVATE_KEY)

	if err != nil {
		return "", err
	}
	return jwt, nil
}
