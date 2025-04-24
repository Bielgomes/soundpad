import asyncio
import json
import os
import signal

import websockets

from global_config import config
from handlers.global_event_handler import GlobalEventHandler


async def echo(websocket: websockets.ServerConnection):
    """
    Handle incoming websocket connections and events.
    This function receives events from the websocket and processes them using the global event handler.

    :param websocket: The websocket connection to handle.
    """

    try:
        while True:
            event = await websocket.recv()
            print(f"📫 Received event: {event}")

            await GlobalEventHandler.handle_event(websocket, json.loads(event))
    except websockets.ConnectionClosed:
        print("❌ Connection closed")
        os.kill(os.getpid(), signal.SIGINT)


async def main():
    async with websockets.serve(echo, config.host, config.port) as server:
        print(f"🚀 Server started on ws://{config.host}:{config.port}")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
