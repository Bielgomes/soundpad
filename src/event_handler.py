import asyncio
import threading
import traceback

import sounddevice as sd
import soundfile as sf
from websockets import ServerConnection

from errors import (
    EventError,
    InvalidSoundFileError,
    MissingFieldError,
    UnsupportedEventError,
)
from events import INCOMING_EVENT_VALUES, ErrorEvent, IncomingEvent, OutgoingEvent
from services.sound import SoundService
from utils import get_output_device, send_message

sound_service = SoundService()


CHUNK_SIZE = 1024

INPUT_VOLUME = 0.5
OUTPUT_VOLUME = 0.5
INPUT_MUTED = False


def play_sound(
    device_id: int,
    sound: sf.SoundFile,
    sound_id: int,
    websocket: ServerConnection,
    loop: asyncio.AbstractEventLoop,
):
    """
    Play sound using sounddevice library on Windows.
    This function creates an input and output stream for the sound file and plays it.

    :param device_id: The ID of the output device to play the sound on.
    :param sound: The sound file to play.
    :param websocket: The websocket connection to send messages to.
    :param loop: The asyncio event loop to run the coroutine in.
    """
    global INPUT_VOLUME, OUTPUT_VOLUME, INPUT_MUTED, CHUNK_SIZE

    input_device_stream = sd.OutputStream(
        blocksize=CHUNK_SIZE,
        samplerate=sound.samplerate,
        channels=sound.channels,
        dtype="float32",
    )
    output_device_stream = sd.OutputStream(
        device=device_id,
        blocksize=CHUNK_SIZE,
        samplerate=sound.samplerate,
        channels=sound.channels,
        dtype="float32",
    )

    input_device_stream.start()
    output_device_stream.start()

    streamed = 0
    sound_size = len(sound)
    while streamed < sound_size:
        chunk = sound.read(CHUNK_SIZE, dtype="float32")
        if len(chunk) == 0:
            break

        input_device_stream.write(chunk * (INPUT_VOLUME if not INPUT_MUTED else 0))
        output_device_stream.write(chunk * OUTPUT_VOLUME)

        streamed += CHUNK_SIZE

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


async def event_handler(websocket: ServerConnection, event: dict):
    """
    Handle events received from the websocket connection.

    This function checks the event type and performs the corresponding action.

    :param websocket: The websocket connection to send the message to.
    :param event: The event received from the client.
    """
    try:
        if event["type"] not in INCOMING_EVENT_VALUES:
            raise UnsupportedEventError(event["type"])

        if event["type"] == IncomingEvent.SOUND_ADD:
            sound = event.get("data", None)
            if sound is None:
                raise MissingFieldError("data")

            new_sound_id = sound_service.create(sound)
            await send_message(
                websocket,
                {
                    "type": OutgoingEvent.SOUND_ADDED,
                    "soundId": new_sound_id,
                },
            )

        elif event["type"] == IncomingEvent.SOUND_REMOVE:
            sound_id = event.get("soundId", None)
            if sound_id is None:
                raise MissingFieldError("soundId")

            sound_service.remove(sound_id)
            await send_message(
                websocket,
                {
                    "type": OutgoingEvent.SOUND_REMOVED,
                    "soundId": sound_id,
                },
            )

        elif event["type"] == IncomingEvent.SOUND_FETCH:
            sounds = sound_service.get_all()
            await send_message(
                websocket,
                {
                    "type": OutgoingEvent.SOUND_FETCHED,
                    "sounds": sounds,
                },
            )

        elif event["type"] == IncomingEvent.SOUND_PLAY:
            sound_id = event.get("soundId", None)
            if sound_id is None:
                raise MissingFieldError("soundId")

            sound = sound_service.get(sound_id)

            try:
                sound_file = sf.SoundFile(sound.path)
            except Exception:
                raise InvalidSoundFileError(sound.path)

            output_device = await get_output_device()
            thread = threading.Thread(
                target=play_sound,
                args=(
                    output_device,
                    sound_file,
                    sound.id,
                    websocket,
                    asyncio.get_event_loop(),
                ),
            )
            thread.start()

            await send_message(
                websocket,
                {"type": OutgoingEvent.SOUND_PLAYING, "soundId": 1},
            )

        elif event["type"] == IncomingEvent.SOUND_STOP:
            sound_id = event.get("soundId", None)
            if sound_id is None:
                raise MissingFieldError("soundId")

            await send_message(
                websocket,
                {
                    "type": OutgoingEvent.SOUND_STOPPED,
                    "soundId": sound_id,
                },
            )

    except EventError as error:
        await send_message(
            websocket,
            {
                "type": error.type,
                "error": str(error),
            },
        )
    except Exception as error:
        print(traceback.format_exc())
        await send_message(
            websocket,
            {
                "type": ErrorEvent.GENERIC_ERROR,
                "error": str(error),
            },
        )
