from models.sound import Sound
from repositories.sound import SoundRepository


class SoundService:
    """
    Service for managing sound records.
    """

    __sound_repository: SoundRepository = SoundRepository()

    def create(self, sound: dict) -> int:
        """
        Create a new sound record.
        """
        try:
            new_sound = Sound.model_validate(sound)
        except Exception as error:
            raise Exception(f"Invalid sound data: {error}")

        return self.__sound_repository.create(new_sound)

    def get_all(self) -> list[dict]:
        """
        Get all sound records.
        """
        sounds = [
            sound.model_dump_json() for sound in self.__sound_repository.get_all()
        ]
        return sounds

    def get(self, id: int) -> Sound:
        """
        Get a sound record by ID.
        """
        sound = self.__sound_repository.get(id)
        if not sound:
            raise Exception(f"Sound with ID {id} not found")

        return sound

    def update(self, id: int, sound: dict) -> None:
        """
        Update a sound record by ID.
        """
        try:
            updated_sound = Sound.model_validate(sound)
        except Exception as error:
            raise Exception(f"Invalid sound data: {error}")

        self.__sound_repository.update(id, updated_sound)

    def delete(self, id: int) -> None:
        """
        Delete a sound record by ID.
        """
        sound = self.__sound_repository.get(id)
        if not sound:
            raise Exception(f"Sound with ID {id} not found")

        self.__sound_repository.delete(id)
