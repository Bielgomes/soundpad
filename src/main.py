import asyncio
import json
import os
import signal
import threading
import traceback

import sounddevice as sd
import soundfile as sf
from websockets import ConnectionClosed, ServerConnection, serve

from services.sound import SoundService

sound_service = SoundService()

HOST = "localhost"
PORT = 4358

CHUNK_SIZE = 1024

INPUT_VOLUME = 0.5
OUTPUT_VOLUME = 0.5
INPUT_MUTED = False

ALLOWED_EVENTS = {"PLAY_SOUND"}


async def get_output_device():
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
    while streamed < len(sound):
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


async def send_message(websocket: ServerConnection, message: json):
    """
    Send a message to the client.

    :param websocket: The websocket connection to send the message to.
    :param message: The message to send.
    """
    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary")

    await websocket.send(json.dumps(message))


async def message_handler(websocket: ServerConnection):
    """
    Handle incoming messages from the websocket connection.

    :param websocket: The websocket connection to handle messages from.
    """

    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            await event_handler(websocket, json.loads(message))
    except ConnectionClosed:
        print("Connection closed")
        os.kill(os.getpid(), signal.SIGINT)


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
    except Exception as error:
        print(traceback.format_exc())
        await send_message(
            websocket,
            {
                "type": "ERROR",
                "error": str(error),
            },
        )


async def main():
    async with serve(message_handler, HOST, PORT) as server:
        print(f"🚀 Server started on ws://{HOST}:{PORT}")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
