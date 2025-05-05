import os
import sqlite3
from typing import Union


class SQLite:
    """
    SQLite class to manage the database connection.
    """

    _instance: Union["SQLite", None] = None

    def __init__(self, db_path: str) -> None:
        """
        Initialize the SQLite class.

        :param db_path: Path to the SQLite database file.
        """

        if SQLite._instance is not None:
            raise Exception("This class is a singleton!")

        SQLite._instance = self
        if not os.path.exists(db_path.rsplit("/", 1)[0]):
            os.makedirs(db_path.rsplit("/", 1)[0])

        self.db_path = db_path

        self.__initialize_database()

    def connection(self: "SQLite") -> sqlite3.Connection:
        """
        Get the SQLite connection.
        """

        return sqlite3.connect(self._instance.db_path)

    def __initialize_database(self) -> None:
        """
        Initialize the database and create the tables if they do not exist.
        """

        print("✨ Initializing database...")
        with self.connection() as connection:
            cursor = connection.cursor()

            sound_table = """
            CREATE TABLE IF NOT EXISTS sound (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                path VARCHAR(255) NOT NULL,
                is_valid BOOLEAN NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """

            config_table = """
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_volume REAL NOT NULL,
                output_volume REAL NOT NULL,
                input_muted BOOLEAN NOT NULL
            );
            """

            cursor.execute(sound_table)
            cursor.execute(config_table)

            cursor.execute("SELECT COUNT(*) FROM config")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute(
                    """
                    INSERT INTO config (input_volume, output_volume, input_muted)
                    VALUES (0.5, 0.5, 0)
                    """
                )

            connection.commit()
            print("✅ Database initialized successfully!")


sqlite = SQLite(f"{os.getenv('APPDATA')}/soundpad/database.db")
