package models

import (
	"github.com/google/uuid"
)

type Apiary struct {
	Name      string
	Location  string
	HoneyKind string
	HiveCount int
	PublicId  uuid.UUID
}
