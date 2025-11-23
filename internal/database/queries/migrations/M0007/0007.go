package M0007

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
)

func Upgrade(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, `
		ALTER TABLE COMMENT RENAME TO COMMENT_OLD;
	`)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS COMMENT (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
			date DATE NOT NULL,
			type BLOB NOT NULL,
			body BLOB NOT NULL,
			hive_id INTEGER NULL,
			apiary_id INTEGER NULL,
			FOREIGN KEY(hive_id) REFERENCES HIVE(id)
			FOREIGN KEY(apiary_id) REFERENCES APIARY(id)
		);
    `)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
		INSERT INTO COMMENT
		SELECT *, null as apiary_id FROM COMMENT_OLD;
    `)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
		DROP TABLE COMMENT_OLD;
    `)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	return nil
}

func Downgrade(ctx context.Context, db *sql.DB) error {
	_, err := db.ExecContext(ctx, `
		ALTER TABLE COMMENT RENAME TO COMMENT_OLD;
	`)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
        CREATE TABLE IF NOT EXISTS COMMENT (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
			public_id BLOB NOT NULL UNIQUE,
			date DATE NOT NULL,
			type BLOB NOT NULL,
			body BLOB NOT NULL,
			hive_id INTEGER NULL,
			FOREIGN KEY(hive_id) REFERENCES HIVE(id)
		);
    `)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
		INSERT INTO COMMENT
		SELECT * FROM COMMENT_OLD;
    `)
	if err != nil {
		return errors.New(fmt.Sprintf("Migration rollbacked: %s", err))
	}

	_, err = db.ExecContext(ctx, `
		DELETE TABLE COMMENT_OLD;
    `)

	return nil
}
