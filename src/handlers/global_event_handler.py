import traceback

import websockets

from handlers.sound_handler import (
    handle_sound_add,
    handle_sound_fetch,
    handle_sound_play,
    handle_sound_remove,
    handle_sound_stop,
)
from utils.errors import (
    EventError,
    MissingFieldError,
    UnsupportedEventError,
)
from utils.events import ErrorEvent, IncomingEvent
from utils.functions import send_message

handlers = {
    IncomingEvent.SOUND_ADD: handle_sound_add,
    IncomingEvent.SOUND_REMOVE: handle_sound_remove,
    IncomingEvent.SOUND_FETCH: handle_sound_fetch,
    IncomingEvent.SOUND_PLAY: handle_sound_play,
    IncomingEvent.SOUND_STOP: handle_sound_stop,
}


async def global_event_handler(websocket: websockets.ServerConnection, event: dict):
    """
    Handle events received from the websocket connection.

    This function checks the event type and performs the corresponding action.

    :param websocket: The websocket connection to send the message to.
    :param event: The event received from the client.
    """
    try:
        if not event.get("type"):
            raise MissingFieldError("type")

        handler = handlers.get(event["type"])
        if handler is None:
            raise UnsupportedEventError(event["type"])

        await handler(websocket, event)

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
