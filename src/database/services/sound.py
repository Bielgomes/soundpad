from database.models import Sound, UpdateSound
from database.repositories.sound import SoundRepository
from utils.errors import SoundNotFoundError, ValidationError


class SoundService:
    """
    Service for managing sound records.
    """

    __sound_repository: SoundRepository = SoundRepository()

    def create(self, sound: dict) -> dict:
        """
        Create a new sound record.
        """

        try:
            new_sound = Sound.model_validate(sound)
        except Exception as error:
            raise ValidationError(str(error))

        created_sound = self.__sound_repository.create(new_sound)
        return created_sound.model_dump()

    def get_all(self) -> list[dict]:
        """
        Get all sound records.
        """

        sounds = [sound.model_dump() for sound in self.__sound_repository.get_all()]
        return sounds

    def get(self, id: int) -> Sound:
        """
        Get a sound record by ID.
        """

        sound = self.__sound_repository.get(id)
        if not sound:
            raise SoundNotFoundError(id)

        return sound

    def update(self, id: int, sound: dict) -> dict:
        """
        Update a sound record by ID.
        """

        try:
            sound = UpdateSound.model_validate(sound)
        except Exception as error:
            raise ValidationError(str(error))

        updated_sound = self.__sound_repository.update(id, sound)
        return updated_sound.model_dump()

    def delete(self, id: int) -> None:
        """
        Delete a sound record by ID.
        """

        sound = self.__sound_repository.get(id)
        if not sound:
            raise SoundNotFoundError(id)

        self.__sound_repository.delete(id)

    def set_is_valid(self, id: int, is_valid: bool) -> None:
        """
        Set the validity of a sound record by ID.
        """

        sound = self.__sound_repository.get(id)
        if not sound:
            raise SoundNotFoundError(id)

        self.__sound_repository.set_is_valid(id, is_valid)
        sound.is_valid = is_valid
        return sound.model_dump()
