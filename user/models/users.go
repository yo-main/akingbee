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
