import asyncio
from pathlib import Path

import websockets

from database.models import Sound
from database.services.sound import SoundService
from handlers.global_event_handler import GlobalEventHandler
from sound_controller import sound_controller
from utils.errors import (
    MissingFieldError,
)
from utils.events import IncomingEvent, OutgoingEvent
from utils.functions import send_message

sound_service = SoundService()


def update_sound_validity(sound: Sound, is_valid: bool) -> None:
    sound.is_valid = is_valid
    sound_service.set_is_valid(sound.id, is_valid)


def build_sound_update_message(sound: Sound) -> dict:
    return {
        "type": OutgoingEvent.SOUND_UPDATED,
        "sound": sound.model_dump(),
    }


@GlobalEventHandler.register(IncomingEvent.SOUND_ADD)
async def handle_sound_add(websocket: websockets.ServerConnection, event: dict) -> None:
    sound = event.get("data", None)
    if sound is None:
        raise MissingFieldError("data")

    new_sound = sound_service.create(sound)
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_ADDED, "sound": new_sound},
    )


@GlobalEventHandler.register(IncomingEvent.SOUND_UPDATE)
async def handle_sound_update(
    websocket: websockets.ServerConnection, event: dict
) -> None:
    sound = event.get("data", None)
    if sound is None:
        raise MissingFieldError("data")

    updated_sound = sound_service.update(sound["id"], sound)
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_UPDATED, "sound": updated_sound},
    )


@GlobalEventHandler.register(IncomingEvent.SOUND_REMOVE)
async def handle_sound_remove(
    websocket: websockets.ServerConnection, event: dict
) -> None:
    sound_id = event.get("soundId", None)
    if sound_id is None:
        raise MissingFieldError("soundId")

    sound_service.delete(sound_id)
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_REMOVED, "soundId": sound_id},
    )


@GlobalEventHandler.register(IncomingEvent.SOUND_FETCH)
async def handle_sound_fetch(
    websocket: websockets.ServerConnection, event: dict
) -> None:
    sounds = sound_service.get_all()
    await send_message(
        websocket,
        {"type": OutgoingEvent.SOUND_FETCHED, "sounds": sounds},
    )


@GlobalEventHandler.register(IncomingEvent.SOUND_PLAY)
async def handle_sound_play(
    websocket: websockets.ServerConnection, event: dict
) -> None:
    sound_id = event.get("soundId", None)
    if sound_id is None:
        raise MissingFieldError("soundId")

    sound = sound_service.get(sound_id)
    if Path(sound.path).is_file():
        if not sound.is_valid:
            update_sound_validity(sound, True)
            await send_message(websocket, build_sound_update_message(sound))
    else:
        if sound.is_valid:
            update_sound_validity(sound, False)
            await send_message(websocket, build_sound_update_message(sound))

        return

    await sound_controller.play_sound(
        sound.path, sound_id, websocket, asyncio.get_event_loop()
    )


@GlobalEventHandler.register(IncomingEvent.SOUND_STOP)
async def handle_sound_stop(websocket: websockets.ServerConnection, _) -> None:
    sound_controller.stop_sound()
