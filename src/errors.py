from events import ErrorEvent


class EventError(Exception):
    """Base class for all Soundpad-related exceptions."""

    def __init__(self, message: str):
        super().__init__(message)
        self.type = ErrorEvent.GENERIC_ERROR


class MissingFieldError(EventError):
    """Exception raised when a required field is missing in the event."""

    def __init__(self, field_name: str):
        super().__init__(f"Missing required field: {field_name}")
        self.type = ErrorEvent.MISSING_FIELD


class ValidationError(EventError):
    """Exception raised when validation fails."""

    def __init__(self, message: str):
        super().__init__(message)
        self.type = ErrorEvent.VALIDATION_ERROR


class InvalidSoundFileError(EventError):
    """Raised when the sound file can't be loaded."""

    def __init__(self, path: str):
        super().__init__(f"Sound file not found or invalid: {path}")
        self.type = ErrorEvent.SOUND_FILE_NOT_FOUND


class SoundNotFoundError(EventError):
    """Raised when the sound is not found."""

    def __init__(self, sound_id: int):
        super().__init__(f"Sound with ID {sound_id} not found")
        self.type = ErrorEvent.SOUND_NOT_FOUND


class UnsupportedEventError(EventError):
    """Raised when the event type is not supported."""

    def __init__(self, event_type: str):
        super().__init__(f"Event type {event_type} not supported")
        self.type = ErrorEvent.EVENT_NOT_SUPPORTED
