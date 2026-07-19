from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field


class ProgSpot(BaseModel):
    model_config = ConfigDict(extra="ignore")
    prog_artist_id: int | None = None
    spot_artist_id: str | None = None

    prog_album_id: int | None = None
    spot_album_id: str | None = None

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
