from pydantic import BaseModel


class AudioModificationRequest(BaseModel):
    speed: float = 1.0
    volume: float = 1.0
