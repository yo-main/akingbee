package models

import (
	"github.com/google/uuid"
)

type Apiary struct {
	name      string
	location  string
	honeyKind string
	hiveCount int
	publicId  uuid.UUID
}
