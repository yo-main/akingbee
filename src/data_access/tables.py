from src.data_access.connectors import MySQL


class Table:

    @staticmethod
    def _create_tables():
        conn = MySQL()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            users(
                id INT AUTO_INCREMENT,
                username TEXT,
                pwd TEXT,
                email TEXT,
                date_last_connection DATETIME,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            beehouse_actions(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (user) REFERENCES users(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            comments_type(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id)
            );
            """
        )
        cursor.execute(
            """
            INSERT INTO
                comments_type(id, en, fr, date_creation, date_modification)
            VALUES
                (1, "User", "Utilisateur", "2019-01-01 00:00:00", "2019-01-01
            00:00:00"),
                (2, "System", "Système", "2019-01-01 00:00:00", "2019-01-01
            00:00:00"),
                (3, "Action", "Action", "2019-01-01 00:00:00", "2019-01-01
            00:00:00");
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            health(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            honey_type(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            owner(
                id INT AUTO_INCREMENT,
                name TEXT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            status_actions(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id)
            );
            """
        )
        cursor.execute(
            """
            INSERT INTO
                status_action(id, en, fr, date_creation, date_modification)
            VALUES
                (1, "Pending", "En attente", "2019-01-01 00:00:00", "2019-01-01
            00:00:00"),
                (2, "Done", "Terminé", "2019-01-01 00:00:00", "2019-01-01
            00:00:00");
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            status_apiary(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            status_beehouse(
                id INT AUTO_INCREMENT,
                fr TEXT,
                en TEXT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            apiary(
                id INT AUTO_INCREMENT,
                name TEXT,
                location TEXT,
                birthday DATETIME,
                status INT,
                honey_type INT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (status) REFERENCES status_apiary(id),
                FOREIGN KEY (honey_type) REFERENCES honey_type(id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            beehouse(
                id INT AUTO_INCREMENT,
                name TEXT,
                birthday DATETIME,
                apiary INT,
                status INT,
                health INT,
                owner INT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (apiary) REFERENCES apiary(id),
                FOREIGN KEY (status) REFERENCES status_beehouse(id),
                FOREIGN KEY (health) REFERENCES health(id),
                FOREIGN KEY (owner) REFERENCES owner(id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            actions(
                id INT AUTO_INCREMENT,
                beehouse INT,
                date DATETIME,
                deadline DATETIME,
                date_done DATETIME,
                type INT,
                status INT,
                user INT,
                comment TEXT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (beehouse) REFERENCES beehouse(id),
                FOREIGN KEY (type) REFERENCES beehouse_actions(id),
                FOREIGN KEY (status) REFERENCES status_actions(id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            comments(
                id INT AUTO_INCREMENT,
                date DATETIME,
                comment TEXT,
                beehouse INT,
                apiary INT,
                health INT,
                action INT,
                type INT,
                user INT,
                date_creation DATETIME,
                date_modification DATETIME,
                PRIMARY KEY (id),
                FOREIGN KEY (beehouse) REFERENCES beehouse(id),
                FOREIGN KEY (apiary) REFERENCES apiary(id),
                FOREIGN KEY (health) REFERENCES health(id),
                FOREIGN KEY (action) REFERENCES actions(id),
                FOREIGN KEY (type) REFERENCES comments_type(id),
                FOREIGN KEY (user) REFERENCES users(id)
            );
            """
        )

        conn.commit()



