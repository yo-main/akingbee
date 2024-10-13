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
	apiary    *Apiary
	swarm     *Swarm
	User      uuid.UUID
}

func (hive *Hive) GetApiaryPublicId() *uuid.UUID {
	if hive.apiary == nil {
		return nil
	}

	return &hive.apiary.PublicId
}

func (hive *Hive) GetApiaryName() string {
	if hive.apiary == nil {
		return "Stock"
	}

	return hive.apiary.Name
}

func (hive *Hive) SetApiary(apiary *Apiary) {
	hive.apiary = apiary
}

func (hive *Hive) GetSwarmPublicId() *uuid.UUID {
	if hive.swarm == nil {
		return nil
	}

	return &hive.swarm.PublicId
}

func (hive *Hive) GetSwarmHealth() string {
	if hive.swarm == nil {
		return ""
	}

	return hive.swarm.Health
}

func (hive *Hive) SetSwarm(swarm *Swarm) {
	hive.swarm = swarm
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
