import asyncio
import threading
import traceback

import sounddevice as sd
import soundfile as sf
from websockets import ServerConnection

from services.sound import SoundService
from utils import get_output_device, send_message

sound_service = SoundService()
ALLOWED_EVENTS = {"PLAY_SOUND", "FETCH_SOUNDS"}


def play_sound(
    device_id: int,
    sound: sf.SoundFile,
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
                "type": "SOUND_FINISHED",
                "sound_id": 1,
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
        if event["type"] not in ALLOWED_EVENTS:
            await send_message(
                websocket,
                {
                    "type": "ERROR",
                    "error": f"Event type {event['type']} not supported",
                },
            )
            return

        if event["type"] == "PLAY_SOUND":
            filename = "./src/sounds/toma-milk-shake-de-morango.mp3"
            sound = sf.SoundFile(filename)

            output_device = await get_output_device()
            thread = threading.Thread(
                target=play_sound,
                args=(output_device, sound, websocket, asyncio.get_event_loop()),
            )
            thread.start()

            await send_message(
                websocket,
                {"type": "PLAYING_SOUND", "sound_id": 1},
            )
        elif event["type"] == "FETCH_SOUNDS":
            sounds = sound_service.get_all()
            await send_message(
                websocket,
                {
                    "type": "SOUNDS_LIST",
                    "sounds": sounds,
                },
            )
    except Exception as error:
        print(traceback.format_exc())
        await send_message(
            websocket,
            {
                "type": "ERROR",
                "error": str(error),
            },
        )
