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
            SELECT id, input_volume, output_volume, input_muted
            FROM config
            WHERE id = 1
            """
        )
        row = self._cursor.fetchone()
        if row:
            return Config(
                id=row[0], input_volume=row[1], output_volume=row[2], input_muted=row[3]
            )

        return None

    def update(self, config: Config) -> None:
        self._cursor.execute(
            """
            UPDATE config
            SET input_volume = ?, output_volume = ?, input_muted = ?
            WHERE id = 1
            """,
            (config.input_volume, config.output_volume, config.input_muted),
        )
        self._commit()
