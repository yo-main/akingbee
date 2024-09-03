package database

import (
	_ "akingbee/app/core/database/queries/migrations"
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
)

func GetDb() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", "akingbee.db")
	if err != nil {
		log.Fatalf("Couldn't open sqlite database: %s\n", err)
		return nil, err
	}

	err = db.Ping()
	if err != nil {
		log.Fatalf("Ping failed: %s\n", err)
		return nil, err
	}

	return db, nil
}
