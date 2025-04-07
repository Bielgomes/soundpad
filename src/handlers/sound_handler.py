import asyncio
import threading

import soundfile as sf
import websockets

from database.services.sound import SoundService
from utils.errors import (
    InvalidSoundFileError,
    MissingFieldError,
)
from utils.events import OutgoingEvent
from utils.functions import get_output_device, play_sound, send_message

sound_service = SoundService()


async def handle_sound_add(websocket: websockets.ServerConnection, event: dict):
    sound = event.get("data", None)
    if sound is None:
        raise MissingFieldError("data")

    new_sound_id = sound_service.create(sound)
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_ADDED, "soundId": new_sound_id},
    )


async def handle_sound_remove(websocket: websockets.ServerConnection, event: dict):
    sound_id = event.get("soundId", None)
    if sound_id is None:
        raise MissingFieldError("soundId")

    sound_service.remove(sound_id)
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_REMOVED, "soundId": sound_id},
    )


async def handle_sound_fetch(websocket: websockets.ServerConnection, event: dict):
    sounds = sound_service.get_all()
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_FETCHED, "sounds": sounds},
    )


async def handle_sound_play(websocket: websockets.ServerConnection, event: dict):
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
        {"type": OutgoingEvent.SOUND_PLAYING, "soundId": sound_id},
    )


async def handle_sound_stop(websocket: websockets.ServerConnection, event: dict):
    sound_id = event.get("soundId", None)
    if sound_id is None:
        raise MissingFieldError("soundId")

    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_STOPPED, "soundId": sound_id},
    )
