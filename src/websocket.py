import asyncio
import json
import os
import signal
import sqlite3
import traceback

from websockets import ConnectionClosed, ServerConnection, serve

with sqlite3.connect("database.db") as connection:
    cursor = connection.cursor()

    sound_table = """
    CREATE TABLE IF NOT EXISTS Sound (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(sound_table)
    connection.commit()


async def send_message(websocket: ServerConnection, message: json):
    await websocket.send(json.dumps(message))


async def handler(websocket: ServerConnection):
    while True:
        try:
            message = await websocket.recv()
            print(f"Received message: {message}")
            await websocket.send(message)
            await event_handler(websocket, json.loads(message))
        except ConnectionClosed:
            os.kill(os.getpid(), signal.SIGINT)
        except Exception as error:
            print(traceback.format_exc())
            await send_message(
                websocket,
                {
                    "type": "ERROR",
                    "error": str(error),
                },
            )
        finally:
            await websocket.close()
            print("Connection closed")


async def event_handler(websocket: ServerConnection, event: dict):
    print(f"Event: {event}")


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
