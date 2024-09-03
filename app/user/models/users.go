package models

import (
	uuid "github.com/google/uuid"
)

type User struct {
	PublicId    uuid.UUID
	Email       string
	Credentials Credentials
}

type Credentials struct {
	PublicId uuid.UUID
	Username string
	Password string
}
