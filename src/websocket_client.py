import asyncio
import json

from websockets import ServerConnection, connect


async def send_message(websocket: ServerConnection, message: json):
    await websocket.send(json.dumps(message))


async def hello():
    async with connect("ws://localhost:8001") as websocket:
        await send_message(
            websocket,
            {
                "type": "ECHO",
                "message": "Hello, server!",
            },
        )
        message = await websocket.recv()
        print(f"Received message: {message}")


if __name__ == "__main__":
    asyncio.run(hello())
