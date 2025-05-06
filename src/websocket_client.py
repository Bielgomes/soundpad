import asyncio
import json

from websockets import connect

from utils.events import IncomingEvent
from utils.functions import send_message


async def hello():
    async with connect("ws://localhost:4358") as websocket:
        await send_message(
            websocket,
            {
                "type": IncomingEvent.SOUND_FETCH,
            },
        )

        all_sounds = json.loads(await websocket.recv())
        first_sound = all_sounds["sounds"][1]["id"] if all_sounds else None

        # await send_message(
        #     websocket,
        #     {
        #         "type": IncomingEvent.SOUND_ADD,
        #         "data": {
        #             "name": "plakton-augh",
        #             "path": "C:\\Users\\Gabriel\\Music\\audios\\plankton-oooooh.mp3",
        #         },
        #     },
        # )

        await send_message(
            websocket,
            {
                "type": IncomingEvent.SOUND_PLAY,
                "soundId": first_sound,
            },
        )

        await asyncio.sleep(1)
        await send_message(
            websocket,
            {
                "type": IncomingEvent.CONFIG_UPDATE,
                "config": {
                    "headphone_volume": 0.1,
                    "microphone_volume": 0.1,
                    "headphone_muted": False,
                },
            },
        )

        await asyncio.sleep(1)
        await send_message(
            websocket,
            {
                "type": IncomingEvent.CONFIG_UPDATE,
                "config": {
                    "headphone_volume": 0.2,
                    "microphone_volume": 0.2,
                    "headphone_muted": True,
                },
            },
        )

        await asyncio.sleep(1)
        await send_message(
            websocket,
            {
                "type": IncomingEvent.CONFIG_UPDATE,
                "config": {
                    "headphone_volume": 0.5,
                    "microphone_volume": 0.5,
                    "headphone_muted": False,
                },
            },
        )

        while True:
            try:
                message = await websocket.recv()
                print(f"Received message: {message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


if __name__ == "__main__":
    asyncio.run(hello())
