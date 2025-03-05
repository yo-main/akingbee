package config

import (
	"log"
	"os"
	"strconv"
)

func getEnv(key string, defaultValue string) string {
	if value, exist := os.LookupEnv(key); exist {
		return value
	}

	return defaultValue
}

func toInt(value string) int {
	valueInt, err := strconv.Atoi(value)
	if err != nil {
		log.Fatalf("Can't read configuration for %s correctly: %s", value, err)
	}

	return valueInt
}

var AppPrivateKey = []byte(getEnv("APP_PRIVATE_KEY", "VERY_PRIVATE_KEY"))
var TokenTTL = toInt(getEnv("TOKEN_TTL", "300000")) // in nanoseconds
