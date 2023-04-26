from datetime import datetime
from pydantic import BaseModel, Extra, Field


class ProgSpot(BaseModel, extra=Extra.ignore):
    prog_artist_id: int = None
    spot_artist_id: str = None

    prog_album_id: int = None
    spot_album_id: str = None

    updated_at: datetime = Field(default_factory=datetime.utcnow)
