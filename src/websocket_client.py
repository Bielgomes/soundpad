import asyncio
import json

from websockets import ServerConnection, connect


async def send_message(websocket: ServerConnection, message: json):
    await websocket.send(json.dumps(message))


async def hello():
    async with connect("ws://localhost:4358") as websocket:
        await send_message(
            websocket,
            {
                "type": "PLAY_SOUND",
                "id": 1,
            },
        )
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")


if __name__ == "__main__":
    asyncio.run(hello())
