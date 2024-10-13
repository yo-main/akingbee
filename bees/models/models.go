package models

import (
	"errors"
	"time"

	"github.com/google/uuid"
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

func (hive *Hive) GetApiary() *Apiary {
	return hive.apiary
}

func (hive *Hive) GetSwarm() *Swarm {
	return hive.swarm
}

func (hive *Hive) GetApiaryPublicId() string {
	if hive.apiary == nil {
		return ""
	}

	return hive.apiary.PublicId.String()
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

func (hive *Hive) SetSwarmHealth(health string) error {
	if hive.swarm == nil {
		return errors.New("Can't set swarm health if it does not exist")
	}

	hive.swarm.Health = health
	return nil
}

type Swarm struct {
	PublicId uuid.UUID
	Year     int
	Health   string
}

func NewSwarm(swarmHealth string) *Swarm {
	return &Swarm{
		PublicId: uuid.New(),
		Health:   swarmHealth,
		Year:     time.Now().Year(),
	}
}

type Comment struct {
	PublicId     uuid.UUID
	Date         time.Time
	Type         string
	Body         string
	HivePublicId *uuid.UUID
}
