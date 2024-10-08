package models

import (
	"github.com/google/uuid"
	"time"
)

type Apiary struct {
	Name      string
	Location  string
	HoneyKind string
	HiveCount int
	PublicId  uuid.UUID
	User      uuid.UUID
}

type Hive struct {
	Name      string
	PublicId  uuid.UUID
	Beekeeper string
	Apiary    *Apiary
	Swarm     *Swarm
	User      uuid.UUID
}

type Swarm struct {
	PublicId uuid.UUID
	Year     int
	Health   string
}

type Comment struct {
	PublicId     uuid.UUID
	Date         time.Time
	Type         string
	Body         string
	HivePublicId *uuid.UUID
}
