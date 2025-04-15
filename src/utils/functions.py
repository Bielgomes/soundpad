import json

import websockets


async def send_message(websocket: websockets.ServerConnection, message: json) -> None:
    """
    Send a message to the client.

    :param websocket: The websocket connection to send the message to.
    :param message: The message to send.
    """

    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary")

    await websocket.send(json.dumps(message))
