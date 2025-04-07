import asyncio

from websockets import connect

from events import IncomingEvent
from utils import send_message


async def hello():
    async with connect("ws://localhost:4358") as websocket:
        await send_message(
            websocket,
            {
                "type": IncomingEvent.SOUND_FETCH,
            },
        )

        # await send_message(
        #     websocket,
        #     {
        #         "type": IncomingEvent.SOUND_ADD,
        #         "data": {
        #             "name": "test",
        #             "path": ".\src\sounds\toma-milk-shake-de-morango.mp3",
        #         },
        #     },
        # )

        await send_message(
            websocket,
            {
                "type": IncomingEvent.SOUND_PLAY,
                "soundId": 2,
            },
        )

        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")


if __name__ == "__main__":
    asyncio.run(hello())
