import asyncio

import soundfile as sf
import websockets

from database.services.sound import SoundService
from sound_controller import sound_controller
from utils.errors import (
    InvalidSoundFileError,
    MissingFieldError,
)
from utils.events import OutgoingEvent
from utils.functions import send_message

sound_service = SoundService()


async def handle_sound_add(websocket: websockets.ServerConnection, event: dict):
    sound = event.get("data", None)
    if sound is None:
        raise MissingFieldError("data")

    new_sound = sound_service.create(sound)
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_ADDED, "sound": new_sound},
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
        sf.SoundFile(sound.path)
    except Exception:
        raise InvalidSoundFileError(sound.path)

    await sound_controller.play_sound(
        sound.path, sound_id, websocket, asyncio.get_event_loop()
    )


async def handle_sound_stop(websocket: websockets.ServerConnection, event: dict):
    sound_controller.stop_sound()
