from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ProgSpot(BaseModel, extra="ignore"):
    prog_artist_id: int = None
    spot_artist_id: str = None

    prog_album_id: int = None
    spot_album_id: str = None

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
