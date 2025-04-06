from lib.sqlite import sqlite


class AbstractRepository:
    """
    Abstract base class for repositories.
    """

    def __init__(self):
        """
        Initialize the repository with a connection to the database.
        """
        self.__conn = sqlite.connection()
        self._cursor = self.__conn.cursor()

    def _commit(self):
        """
        Commit the current transaction to the database.
        """
        self.__conn.commit()
