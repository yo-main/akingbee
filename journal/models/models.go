package models

import (
	"time"

	"github.com/google/uuid"
)

type Comment struct {
	PublicID       uuid.UUID
	Date           time.Time
	Type           string
	Body           string
	HivePublicID   *uuid.UUID
	ApiaryPublicID *uuid.UUID
}
