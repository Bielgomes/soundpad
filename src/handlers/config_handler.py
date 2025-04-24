import websockets

from database.services.config import ConfigService
from global_config import config as global_config
from handlers.global_event_handler import GlobalEventHandler
from utils.errors import MissingFieldError
from utils.events import IncomingEvent, OutgoingEvent
from utils.functions import send_message

config_service = ConfigService()


@GlobalEventHandler.register(IncomingEvent.CONFIG_FETCH)
async def handle_config_fetch(
    websocket: websockets.ServerConnection, event: dict
) -> None:
    config = config_service.get()
    await send_message(
        websocket,
        {
            "type": OutgoingEvent.CONFIG_FETCHED,
            "config": config.model_dump(),
        },
    )


@GlobalEventHandler.register(IncomingEvent.CONFIG_UPDATE)
async def handle_config_update(
    websocket: websockets.ServerConnection, event: dict
) -> None:
    config = event.get("config", None)
    if config is None:
        raise MissingFieldError("config")

    config_service.update(config)

    global_config.input_volume = config.get("input_volume", 0.5)
    global_config.output_volume = config.get("output_volume", 0.5)
    global_config.input_muted = config.get("input_muted", False)

    await send_message(
        websocket,
        {
            "type": OutgoingEvent.CONFIG_UPDATED,
            "config": config,
        },
    )
