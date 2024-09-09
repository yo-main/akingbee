package config

import (
	"log"
	"os"
	"strconv"
)

func getEnv(key string, defaultValue string) string {
	value, exist := os.LookupEnv(key)
	if exist {
		return value
	} else {
		return defaultValue
	}
}

func toInt(value string) int {
	valueInt, err := strconv.Atoi(value)
	if err != nil {
		log.Fatalf("Can't read configuration for %s correctly: %s", value, err)
	}

	return valueInt
}

var APP_PRIVATE_KEY = []byte(getEnv("APP_PRIVATE_KEY", "VERY_PRIVATE_KEY"))
var JWT_TTL = toInt(getEnv("TOKEN_TTL", "300"))
