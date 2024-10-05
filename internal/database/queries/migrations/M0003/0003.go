package M0003

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

func Upgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS SWARM (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
			year INTEGER NOT NULL,
			health BLOB NOT NULL
		);
    `)

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS HIVE (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
            name BLOB NOT NULL UNIQUE,
			beekeeper BLOB NOT NULL,
            apiary_id INTEGER,
			swarm_id INTEGER,
			user_id INTEGER NOT NULL,
			FOREIGN KEY(user_id) REFERENCES USERS(id),
			FOREIGN KEY(apiary_id) REFERENCES APIARY(id),
			FOREIGN KEY(swarm_id) REFERENCES SWARM(id)
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
