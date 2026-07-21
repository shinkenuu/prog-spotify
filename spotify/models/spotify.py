from datetime import date, datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Artist(BaseModel):
    model_config = ConfigDict(extra="ignore")

    progarchives_artist_id: int | None = Field(alias="_progarchives_artist_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=lambda: datetime.now(timezone.utc))

    id: str
    name: str
    popularity: int | None = None

    genres: list[str] = []

    def dict(self, *args, **kwargs):
        _dict = super().model_dump(by_alias=True, *args, **kwargs)
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict


class ArtistRef(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str


class Album(BaseModel):
    model_config = ConfigDict(extra="ignore")
    progarchives_album_id: int | None = Field(alias="_progarchives_album_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=lambda: datetime.now(timezone.utc))

    id: str
    name: str
    release_date: date | None | None = None
    release_date_precision: str | None = None
    total_tracks: int | None = None
    image_url: str | None = Field(alias="images", default=None)
    album_type: str | None = None
    artists: list[ArtistRef] = []

    @field_validator("release_date", mode="before")
    @classmethod
    def parse_release_date(cls, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except Exception:
            return None

    @field_validator("image_url", mode="before")
    @classmethod
    def parse_image_url(cls, value):
        images = value

        if not images:
            return None

        # Handle plain string URL (e.g., from test fixtures)
        if isinstance(images, str):
            return images

        sorted_images = sorted(images, key=lambda _: _["height"] * _["width"])
        bigger_image = sorted_images[-1]

        return bigger_image["url"]

    def dict(self, *args, **kwargs):
        _dict = super().model_dump(by_alias=True, *args, **kwargs)
        _dict['release_date'] = self.release_date.isoformat() if self.release_date else None
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict


class Track(BaseModel):
    model_config = ConfigDict(extra="ignore")
    progarchives_album_id: int = Field(alias="_progarchives_album_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=lambda: datetime.now(timezone.utc))

    id: str
    name: str
    track_number: int | None = None
    disc_number: int | None = None
    release_date_precision: str | None = None
    duration_ms: int | None = None
    explicit: bool | None = None

    artists: list[ArtistRef] = []

    def dict(self, *args, **kwargs):
        _dict = super().model_dump(by_alias=True, *args, **kwargs)
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict


class AudioFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")
    progarchives_album_id: int = Field(alias="_progarchives_album_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=lambda: datetime.now(timezone.utc))

    id: str  # Track ID
    danceability: float | None = None
    energy: float | None = None
    key: int | None = None
    loudness: float | None = None
    mode: int | None = None
    speechiness: float | None = None
    acousticness: float | None = None
    instrumentalness: float | None = None
    liveness: float | None = None
    valence: float | None = None
    tempo: float | None = None
    duration_ms: int | None = None
    time_signature: int | None = None
    analysis_url: str | None = None

    def dict(self, *args, **kwargs):
        _dict = super().model_dump(by_alias=True, *args, **kwargs)
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict
