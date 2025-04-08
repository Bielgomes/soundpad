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
            CREATE TABLE IF NOT EXISTS Sound (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                path VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(sound_table)
            connection.commit()

            print("✅ Database initialized successfully!")


sqlite = SQLite("database.db")
