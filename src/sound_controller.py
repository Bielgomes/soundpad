import asyncio
import threading
from typing import Union

import sounddevice as sd
import soundfile as sf
import websockets

from global_config import config
from utils.errors import VoicemeeterPlaybackDeviceError
from utils.events import OutgoingEvent
from utils.functions import send_message


class SoundController:
    _instance: Union["SoundController", None] = None

    _stop_event: Union[threading.Event, None] = threading.Event()
    _playback_thread: Union[threading.Thread, None] = None

    _sound_file: Union[sf.SoundFile, None] = None
    _streamed: int = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundController, cls).__new__(cls)
        return cls._instance

    def stop_sound(self):
        self._streamed = 0
        self._stop_event.set()

        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join()

        if self._sound_file is not None:
            self._sound_file.close()
            self._sound_file = None

    async def play_sound(
        self,
        sound_path: str,
        sound_id: int,
        websocket: websockets.ServerConnection,
        loop: asyncio.AbstractEventLoop,
    ):
        self.stop_sound()
        self._stop_event.clear()

        output_device = await self.__get_voicemeeter_playback_device()
        self._playback_thread = threading.Thread(
            target=self.__play_sound,
            args=(output_device, sound_path, sound_id, websocket, loop),
        )
        self._playback_thread.start()

    def __play_sound(
        self,
        device_id: int,
        sound_path: str,
        sound_id: int,
        websocket: websockets.ServerConnection,
        loop: asyncio.AbstractEventLoop,
    ):
        self._sound_file = sf.SoundFile(sound_path)

        input_stream = sd.OutputStream(
            blocksize=config.chunk_size,
            samplerate=self._sound_file.samplerate,
            channels=self._sound_file.channels,
            dtype="float32",
        )
        output_stream = sd.OutputStream(
            device=device_id,
            blocksize=config.chunk_size,
            samplerate=self._sound_file.samplerate,
            channels=self._sound_file.channels,
            dtype="float32",
        )

        input_stream.start()
        output_stream.start()

        asyncio.run_coroutine_threadsafe(
            send_message(
                websocket,
                {
                    "type": OutgoingEvent.SOUND_PLAYING,
                    "soundId": sound_id,
                },
            ),
            loop,
        )

        self._streamed = 0
        while self._streamed + config.chunk_size < len(self._sound_file):
            if self._stop_event.is_set():
                break

            chunk = self._sound_file.read(config.chunk_size, dtype="float32")

            input_stream.write(
                chunk * (config.input_volume if not config.input_muted else 0)
            )
            output_stream.write(chunk * config.output_volume)

            self._streamed += config.chunk_size

        self._sound_file = None
        self._streamed = 0

        input_stream.close()
        output_stream.close()

        asyncio.run_coroutine_threadsafe(
            send_message(
                websocket,
                {
                    "type": OutgoingEvent.SOUND_STOPPED,
                    "soundId": sound_id,
                },
            ),
            loop,
        )

    async def __get_voicemeeter_playback_device(self) -> int:
        """
        Get the device ID for sending audio to Voicemeeter.
        """

        devices = sd.query_devices()

        voicemeeter_playback = [
            device["index"]
            for device in devices
            if "voicemeeter input (vb-audio voi" in device["name"].lower()
            and device["hostapi"] == 0
        ]

        if not voicemeeter_playback:
            raise VoicemeeterPlaybackDeviceError("Voicemeeter Input device not found")

        if len(voicemeeter_playback) > 1:
            raise VoicemeeterPlaybackDeviceError(
                "Multiple Voicemeeter Input devices found"
            )

        return voicemeeter_playback[0]


sound_controller = SoundController()
