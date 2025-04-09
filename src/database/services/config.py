from database.models import Config
from database.repositories.config import ConfigRepository
from utils.errors import ConfigNotFoundError, ValidationError


class ConfigService:
    """
    Service for managing config record.
    """

    __config_repository: ConfigRepository = ConfigRepository()

    def get(self) -> Config:
        """
        Get config record.
        """

        config = self.__config_repository.get()
        if not config:
            raise ConfigNotFoundError(1)

        return config

    def update(self, config: dict) -> None:
        """
        Update config record.
        """

        try:
            updated_config = Config.model_validate(config)
        except Exception as error:
            raise ValidationError(str(error))

        self.__config_repository.update(updated_config)
