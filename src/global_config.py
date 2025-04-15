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

        self._input_volume = config.input_volume
        self._output_volume = config.output_volume
        self._input_muted = config.input_muted

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
    def input_volume(self) -> float:
        return self._input_volume

    @input_volume.setter
    def input_volume(self, value: float) -> None:
        if 0 <= value <= 1:
            self._input_volume = value
        else:
            raise ValueError("Volume must be between 0 and 1.")

    @property
    def output_volume(self) -> float:
        return self._output_volume

    @output_volume.setter
    def output_volume(self, value: float) -> None:
        if 0 <= value <= 1:
            self._output_volume = value
        else:
            raise ValueError("Volume must be between 0 and 1.")

    @property
    def input_muted(self) -> bool:
        return self._input_muted

    @input_muted.setter
    def input_muted(self, value: bool) -> None:
        if isinstance(value, bool):
            self._input_muted = value
        else:
            raise ValueError("Muted status must be a boolean.")


config_service = ConfigService()
config = GlobalConfig(config_service.get())
