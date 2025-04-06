import asyncio

from websockets import connect

from utils import send_message


async def hello():
    async with connect("ws://localhost:4358") as websocket:
        await send_message(
            websocket,
            {
                "type": "FETCH_SOUNDS",
                "id": 1,
            },
        )
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")


if __name__ == "__main__":
    asyncio.run(hello())
