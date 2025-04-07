from enum import Enum


class IncomingEvent(str, Enum):
    """
    Enum for incoming events.
    """

    SOUND_ADD = "SOUND:ADD"
    SOUND_REMOVE = "SOUND:REMOVE"
    SOUND_FETCH = "SOUND:FETCH"
    SOUND_PLAY = "SOUND:PLAY"
    SOUND_STOP = "SOUND:STOP"


class OutgoingEvent(str, Enum):
    """
    Enum for outgoing events.
    """

    SOUND_ADDED = "SOUND:ADDED"
    SOUND_REMOVED = "SOUND:REMOVED"
    SOUND_FETCHED = "SOUND:FETCHED"
    SOUND_PLAYING = "SOUND:PLAYING"
    SOUND_STOPPED = "SOUND:STOPPED"


class ErrorEvent(str, Enum):
    """
    Enum for error events.
    """

    GENERIC_ERROR = "ERROR:GENERIC"
    EVENT_NOT_SUPPORTED = "ERROR:EVENT_NOT_SUPPORTED"
    MISSING_FIELD = "ERROR:MISSING_FIELD"
    VALIDATION_ERROR = "ERROR:VALIDATION_ERROR"
    SOUND_FILE_NOT_FOUND = "ERROR:SOUND_FILE_NOT_FOUND"
    SOUND_NOT_FOUND = "ERROR:SOUND_NOT_FOUND"


INCOMING_EVENT_VALUES = {e.value for e in IncomingEvent}
