from typing import Union

from database.models import Sound
from database.repositories.abstract_repository import AbstractRepository


class SoundRepository(AbstractRepository):
    """
    Repository for managing sound records in the database.
    """

    def __init__(self):
        super().__init__()

    def create(self, sound: Sound) -> Sound:
        self._cursor.execute(
            """
            INSERT INTO sound (name, path)
            VALUES (?, ?)
            """,
            (sound.name, sound.path),
        )
        self._commit()

        sound.id = self._cursor.lastrowid
        sound.created_at = self._cursor.execute(
            """
            SELECT created_at
            FROM sound
            WHERE id = ?
            """,
            (sound.id,),
        ).fetchone()[0]

        return sound

    def get_all(self) -> list[Sound]:
        self._cursor.execute(
            """
            SELECT id, name, path, is_valid, created_at
            FROM sound
            """
        )
        rows = self._cursor.fetchall()
        return [
            Sound(
                id=row[0], name=row[1], path=row[2], is_valid=row[3], created_at=row[4]
            )
            for row in rows
        ]

    def get(self, id: int) -> Union[Sound, None]:
        self._cursor.execute(
            """
            SELECT id, name, path, is_valid, created_at
            FROM sound
            WHERE id = ?
            """,
            (id,),
        )
        row = self._cursor.fetchone()
        if row:
            return Sound(
                id=row[0], name=row[1], path=row[2], is_valid=row[3], created_at=row[4]
            )

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

    def set_is_valid(self, id: int, is_valid: bool) -> None:
        self._cursor.execute(
            """
            UPDATE sound
            SET is_valid = ?
            WHERE id = ?
            """,
            (is_valid, id),
        )
        self._commit()
