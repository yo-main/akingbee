package database

import (
	"database/sql"
	"log"
	"sync"

	_ "github.com/mattn/go-sqlite3" // use sqlite for db engine
)

var lock = &sync.Mutex{}
var db *sql.DB

func createDB() (*sql.DB, error) {
	dbClient, err := sql.Open("sqlite3", "akingbee.db")
	if err != nil {
		log.Fatalf("Couldn't open sqlite database: %s\n", err)
		return nil, err
	}

	err = dbClient.Ping()
	if err != nil {
		log.Panicf("Ping failed: %s\n", err)
		return nil, err
	}

	return dbClient, nil
}

func GetDB() *sql.DB {
	if db == nil {
		lock.Lock()
		defer lock.Unlock()

		if db == nil {
			dbInstance, err := createDB()
			if err != nil {
				log.Panicf("Could not get a database instance: %s\n", err)
			}

			db = dbInstance
		}
	}

	return db
}

func CloseRows(rows *sql.Rows) {
	err := rows.Close()

	if err != nil {
		log.Println("Could not close rows: %w", err)
	}
}
