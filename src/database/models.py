from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Sound(BaseModel):
    id: Optional[int] = Field(default=None, title="Sound ID")
    name: str = Field(..., min_length=1, max_length=255, title="Sound Name")
    path: str = Field(..., min_length=1, max_length=255, title="Sound Path")
    created_at: Optional[str] = Field(None, title="Creation Date")

    @field_validator("path")
    @classmethod
    def validate_path(cls, path: str) -> str:
        """
        Validate the sound path to ensure it ends with .mp3 or .wav.
        """

        if not path.endswith((".mp3", ".wav")):
            raise ValueError("Sound path must end with .mp3 or .wav")

        return path


class Config(BaseModel):
    id: Optional[int] = Field(default=None, title="Config ID")
    input_volume: float = Field(default=0.5, ge=0.0, le=1.0, title="Input Volume")
    output_volume: float = Field(default=0.5, ge=0.0, le=1.0, title="Output Volume")
    input_muted: bool = Field(default=False, title="Input Muted")
