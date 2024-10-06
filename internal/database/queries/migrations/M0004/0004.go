package M0004

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

func Upgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS COMMENT (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
			date DATE NOT NULL,
			body BLOB NOT NULL,
			hive_id INTEGER NOT NULL,
			FOREIGN KEY(hive_id) REFERENCES HIVE(id)
		);
    `)

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}

func Downgrade(ctx context.Context, db *sql.DB) error {

	_, err := db.ExecContext(ctx, "DROP TABLE COMMENT")

	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}
