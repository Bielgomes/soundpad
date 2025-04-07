import asyncio
import json

import sounddevice as sd
import soundfile as sf
import websockets

from global_config import config
from utils.events import OutgoingEvent


async def send_message(websocket: websockets.ServerConnection, message: json) -> None:
    """
    Send a message to the client.

    :param websocket: The websocket connection to send the message to.
    :param message: The message to send.
    """
    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary")

    await websocket.send(json.dumps(message))


async def get_output_device() -> int:
    """
    Get the output device ID for Voicemeeter input.
    """
    devices = sd.query_devices()
    voicemeeter_input = [
        device["index"]
        for device in devices
        if "voicemeeter input (vb-audio voi" in device["name"].lower()
        and device["hostapi"] == 0
    ]

    if not voicemeeter_input:
        raise RuntimeError("Voicemeeter input device not found")
    if len(voicemeeter_input) > 1:
        raise RuntimeError("Multiple Voicemeeter input devices found")

    return voicemeeter_input[0]


def play_sound(
    device_id: int,
    sound: sf.SoundFile,
    sound_id: int,
    websocket: websockets.ServerConnection,
    loop: asyncio.AbstractEventLoop,
):
    """
    Play sound using sounddevice library.
    This function creates an input and output stream for the sound file and plays it.

    :param device_id: The ID of the output device to play the sound on.
    :param sound: The sound file to play.
    :param websocket: The websocket connection to send messages to.
    :param loop: The asyncio event loop to run the coroutine in.
    """

    input_device_stream = sd.OutputStream(
        blocksize=config.chunk_size,
        samplerate=sound.samplerate,
        channels=sound.channels,
        dtype="float32",
    )
    output_device_stream = sd.OutputStream(
        device=device_id,
        blocksize=config.chunk_size,
        samplerate=sound.samplerate,
        channels=sound.channels,
        dtype="float32",
    )

    input_device_stream.start()
    output_device_stream.start()

    streamed = 0
    sound_size = len(sound)
    while streamed < sound_size:
        chunk = sound.read(config.chunk_size, dtype="float32")
        if len(chunk) == 0:
            break

        input_device_stream.write(
            chunk * (config.input_volume if not config.input_muted else 0)
        )
        output_device_stream.write(chunk * config.output_volume)

        streamed += config.chunk_size

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
