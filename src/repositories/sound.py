from typing import Union

from models.sound import Sound
from repositories.abstract_repository import AbstractRepository


class SoundRepository(AbstractRepository):
    """
    Repository for managing sound records in the database.
    """

    def __init__(self):
        super().__init__()

    def create(self, sound: Sound) -> None:
        self._cursor.execute(
            """
            INSERT INTO sound (name, path)
            VALUES (?, ?)
            """,
            (sound.name, sound.path),
        )
        self._commit()

    def get_all(self) -> list[Sound]:
        self._cursor.execute(
            """
            SELECT id, name, path, created_at
            FROM sound
            """
        )
        rows = self._cursor.fetchall()
        return [
            Sound(id=row[0], name=row[1], path=row[2], created_at=row[3])
            for row in rows
        ]

    def get(self, id: int) -> Union[Sound, None]:
        self._cursor.execute(
            """
            SELECT id, name, path, created_at
            FROM sound
            WHERE id = ?
            """,
            (id,),
        )
        row = self._cursor.fetchone()
        if row:
            return Sound(id=row[0], name=row[1], path=row[2], created_at=row[3])

        return None

    def update(self, sound: Sound) -> None:
        self._cursor.execute(
            """
            UPDATE sound
            SET name = ?, path = ?
            WHERE id = ?
            """,
            (sound.name, sound.path, sound.id),
        )
        self._commit()

    def delete(self, id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM sound
            WHERE id = ?
            """,
            (id,),
        )
        self._commit()
