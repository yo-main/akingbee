package M0002

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

func Upgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS APIARY (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
            username BLOB NOT NULL UNIQUE,
            password BLOB NOT NULL
        );
    `)

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}

func Downgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, "DROP TABLE APIARY")

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}
