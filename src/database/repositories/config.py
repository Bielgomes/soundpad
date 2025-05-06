from typing import Union

from database.models import Config
from database.repositories.abstract_repository import AbstractRepository


class ConfigRepository(AbstractRepository):
    """
    Repository for managing config record in the database.
    """

    def __init__(self):
        super().__init__()

    def get(self) -> Union[Config, None]:
        self._cursor.execute(
            """
            SELECT id, headphone_volume, microphone_volume, headphone_muted
            FROM config
            WHERE id = 1
            """
        )
        row = self._cursor.fetchone()
        if row:
            return Config(
                id=row[0],
                headphone_volume=row[1],
                microphone_volume=row[2],
                headphone_muted=row[3],
            )

        return None

    def update(self, config: Config) -> None:
        self._cursor.execute(
            """
            UPDATE config
            SET headphone_volume = ?, microphone_volume = ?, headphone_muted = ?
            WHERE id = 1
            """,
            (config.headphone_volume, config.microphone_volume, config.headphone_muted),
        )
        self._commit()
