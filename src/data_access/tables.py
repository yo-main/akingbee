from src.data_access.connectors import MySQL


class Table:

    @staticmethod
    def _create_tables():

        with MySQL() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS
                users(
                    id INT AUTO_INCREMENT,
                    username TEXT,
                    pwd TEXT,
                    email TEXT,
                    date_last_connection DATE,
                    date_creation DATE,
                    date_modification DATE,
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
                    date_creation DATE,
                    date_modification DATE,
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
                    date_creation DATE,
                    date_modification DATE,
                    PRIMARY KEY (id)
                );
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
                    date_creation DATE,
                    date_modification DATE,
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
                    date_creation DATE,
                    date_modification DATE,
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
                    date_creation DATE,
                    date_modification DATE,
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
                    date_creation DATE,
                    date_modification DATE,
                    PRIMARY KEY (id)
                );
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
                    date_creation DATE,
                    date_modification DATE,
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
                    date_creation DATE,
                    date_modification DATE,
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
                    birthday DATE,
                    status INT,
                    honey_type INT,
                    user INT,
                    date_creation DATE,
                    date_modification DATE,
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
                    birthday DATE,
                    apiary INT,
                    status INT,
                    health INT,
                    owner INT,
                    user INT,
                    date_creation DATE,
                    date_modification DATE,
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
                    date DATE,
                    deadline DATE,
                    date_done DATE,
                    type INT,
                    status INT,
                    user INT,
                    comment TEXT,
                    date_creation DATE,
                    date_modification DATE,
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
                    date DATE,
                    comment TEXT,
                    beehouse INT,
                    apiary INT,
                    health INT,
                    action INT,
                    type INT,
                    user INT,
                    date_creation DATE,
                    date_modification DATE,
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




