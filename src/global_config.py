from typing import Union

from database.models import Config
from database.services.config import ConfigService


class GlobalConfig:
    """
    Singleton class to manage global configuration settings for the application.
    This class is designed to be initialized only once and provides access to configuration settings
    """

    _instance: Union["GlobalConfig", None] = None

    def __new__(cls, config: Config) -> "GlobalConfig":
        if not cls._instance:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls._instance._init(config)

        return cls._instance

    def _init(self, config: Config) -> None:
        self._host = "localhost"
        self._port = 4358

        self._chunk_size = 1024

        self._headphone_volume = config.headphone_volume
        self._microphone_volume = config.microphone_volume
        self.headphone_muted = config.headphone_muted

        print("🔧 Config synced with database: { " + f"{config}" + " }")

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def chunk_size(self) -> int:
        return self._chunk_size

    @property
    def headphone_volume(self) -> float:
        return self._headphone_volume

    @headphone_volume.setter
    def headphone_volume(self, value: float) -> None:
        if 0 <= value <= 1:
            self._headphone_volume = value
        else:
            raise ValueError("Volume must be between 0 and 1.")

    @property
    def microphone_volume(self) -> float:
        return self._microphone_volume

    @microphone_volume.setter
    def microphone_volume(self, value: float) -> None:
        if 0 <= value <= 1:
            self._microphone_volume = value
        else:
            raise ValueError("Volume must be between 0 and 1.")

    @property
    def headphone_muted(self) -> bool:
        return self._headphone_muted

    @headphone_muted.setter
    def headphone_muted(self, value: bool) -> None:
        if isinstance(value, bool):
            self._headphone_muted = value
        else:
            raise ValueError("Muted status must be a boolean.")


config_service = ConfigService()
config = GlobalConfig(config_service.get())
