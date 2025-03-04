package M0002

import (
	"context"
	"database/sql"
	"fmt"
)

func Upgrade(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS APIARY (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
            name BLOB NOT NULL UNIQUE,
            location BLOB NOT NULL,
            honey_kind BLOB NOT NULL,
			user_id INTEGER NOT NULL,
			FOREIGN KEY(user_id) REFERENCES USERS(id)
        );
    `)

	if err != nil {
		return fmt.Errorf("migration rollbacked: %w", err)
	}

	return nil
}

func Downgrade(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, "DROP TABLE APIARY")

	if err != nil {
		return fmt.Errorf("migration rollbacked: %w", err)
	}

	return nil
}
