from enum import Enum


class IncomingEvent(Enum):
    """
    Enum for incoming events.
    """

    SOUND_ADD = "SOUND:ADD"
    SOUND_REMOVE = "SOUND:REMOVE"
    SOUND_FETCH = "SOUND:FETCH"
    SOUND_PLAY = "SOUND:PLAY"
    SOUND_STOP = "SOUND:STOP"


class OutgoingEvent(Enum):
    """
    Enum for outgoing events.
    """

    SOUND_ADDED = "SOUND:ADDED"
    SOUND_REMOVED = "SOUND:REMOVED"
    SOUND_FETCHED = "SOUND:FETCHED"
    SOUND_PLAYING = "SOUND:PLAYING"
    SOUND_STOPPED = "SOUND:STOPPED"
    GENERIC_ERROR = "ERROR:GENERIC"
    EVENT_NOT_SUPPORTED = "ERROR:EVENT_NOT_SUPPORTED"


INCOMING_EVENT_VALUES = {e.value for e in IncomingEvent}
OUTGOING_EVENT_VALUES = {e.value for e in OutgoingEvent}
