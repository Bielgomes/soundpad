import json

import sounddevice as sd
from websockets import ServerConnection


async def send_message(websocket: ServerConnection, message: json):
    """
    Send a message to the client.

    :param websocket: The websocket connection to send the message to.
    :param message: The message to send.
    """
    if not isinstance(message, dict):
        raise ValueError("Message must be a dictionary")

    await websocket.send(json.dumps(message))


async def get_output_device():
    """
    Get the output device ID for Voicemeeter input.
    """
    devices = sd.query_devices()
    voicemeeter_input = [
        device["index"]
        for device in devices
        if "voicemeeter input (vb-audio voi" in device["name"].lower()
        and device["hostapi"] == 0
    ]

    if not voicemeeter_input:
        raise RuntimeError("Voicemeeter input device not found")
    if len(voicemeeter_input) > 1:
        raise RuntimeError("Multiple Voicemeeter input devices found")

    return voicemeeter_input[0]
