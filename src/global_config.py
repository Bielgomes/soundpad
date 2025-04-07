class GlobalConfig:
    __instance = None

    def __new__(cls) -> "GlobalConfig":
        if not cls.__instance:
            cls.__instance = super(GlobalConfig, cls).__new__(cls)
            cls.__instance._init()
        return cls.__instance

    def _init(self) -> None:
        self._host = "localhost"
        self._port = 4358

        self._chunk_size = 1024

        self._input_volume = 0.2
        self._output_volume = 0.2
        self._input_muted = False

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


config = GlobalConfig()
