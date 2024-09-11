package database

import (
	_ "akingbee/internal/database/queries/migrations"
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"sync"
)

var lock = &sync.Mutex{}
var db *sql.DB

func createDb() (*sql.DB, error) {
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

func GetDb() *sql.DB {
	if db == nil {
		lock.Lock()
		defer lock.Unlock()

		if db == nil {
			db_instance, err := createDb()
			if err != nil {
				log.Fatalf("Could not get a database instance: %s", err)
			}
			db = db_instance
		}
	}

	return db
}
