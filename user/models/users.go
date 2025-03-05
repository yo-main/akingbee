package models

import (
	uuid "github.com/google/uuid"
)

type User struct {
	PublicID    uuid.UUID
	Email       string
	Credentials Credentials
}

type Credentials struct {
	PublicID uuid.UUID
	Username string
	Password string
}

func (u *User) IsAdmin() bool {
	return u.Credentials.Username == "Romain"
}

type AuthenticatedUser struct {
	*User
	Impersonator *uuid.UUID
}
