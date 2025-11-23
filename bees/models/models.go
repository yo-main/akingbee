package models

import (
	"errors"
	"strconv"
	"time"

	"github.com/google/uuid"
)

var errSwarmNotFound = errors.New("can't set swarm health if it does not exist")

type Apiary struct {
	Name      string
	Location  string
	HoneyKind string
	HiveCount int
	PublicID  uuid.UUID
	User      uuid.UUID
}

type Hive struct {
	Name      string
	PublicID  uuid.UUID
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

func (hive *Hive) GetApiaryPublicID() string {
	if hive.apiary == nil {
		return ""
	}

	return hive.apiary.PublicID.String()
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

func (hive *Hive) GetSwarmPublicID() *uuid.UUID {
	if hive.swarm == nil {
		return nil
	}

	return &hive.swarm.PublicID
}

func (hive *Hive) GetSwarmHealth() string {
	if hive.swarm == nil {
		return ""
	}

	return hive.swarm.Health
}

func (hive *Hive) GetQueenColor() string {
	if hive.swarm == nil {
		return ""
	}

	var color string
	switch hive.swarm.Year % 10 {
	case 0, 5:
		color = "#34aeeb" // blue
	case 1, 6:
		color = "#bfbfbf" // white
	case 2, 7:
		color = "#e8eb46" // yellow
	case 3, 8:
		color = "#eb746a" // red
	case 4, 9:
		color = "#64d149" // green
	}

	return color
}

func (hive *Hive) GetSwarmYear() string {
	if hive.swarm == nil {
		return ""
	}

	return strconv.Itoa(hive.swarm.Year)
}

func (hive *Hive) SetSwarm(swarm *Swarm) {
	hive.swarm = swarm
}

func (hive *Hive) SetSwarmHealth(health string) error {
	if hive.swarm == nil {
		return errSwarmNotFound
	}

	hive.swarm.Health = health

	return nil
}

func (hive *Hive) SetSwarmYear(year int) error {
	if hive.swarm == nil {
		return errSwarmNotFound
	}

	hive.swarm.Year = year

	return nil
}

type Swarm struct {
	PublicID uuid.UUID
	Year     int
	Health   string
}

func NewSwarm(swarmHealth string) *Swarm {
	return &Swarm{
		PublicID: uuid.New(),
		Health:   swarmHealth,
		Year:     time.Now().Year(),
	}
}

type Harvest struct {
	PublicID     uuid.UUID
	Date         time.Time
	Quantity     int
	HivePublicID *uuid.UUID
}
