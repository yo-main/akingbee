package M0003

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

func Upgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS HIVE (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
            name BLOB NOT NULL UNIQUE,
			condition BLOB NOT NULL,
            apiary_id INTEGER,
			owner_id INTEGER NOT NULL,
			FOREIGN KEY(owner_id) REFERENCES USERS(id)
			FOREIGN KEY(apiary_id) REFERENCES APIARY(id)
        );
    `)

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS SWARM (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
			year INTEGER NOT NULL,
			health BLOB NOT NULL,
			hive_id INTEGER NOT NULL UNIQUE,
			FOREIGN KEY(hive_id) REFERENCES HIVE(id)
		);
    `)

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}

func Downgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, "DROP TABLE SWARM")

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, "DROP TABLE HIVE")

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}
