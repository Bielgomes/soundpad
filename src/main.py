import asyncio
import json
import os
import signal

from websockets import ConnectionClosed, ServerConnection, serve

from event_handler import event_handler

HOST = "localhost"
PORT = 4358


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


async def main():
    async with serve(message_handler, HOST, PORT) as server:
        print(f"🚀 Server started on ws://{HOST}:{PORT}")
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
