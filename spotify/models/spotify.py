from datetime import date, datetime
from pydantic import BaseModel, Extra, Field, validator


class Artist(BaseModel, extra=Extra.ignore):
    progarchives_artist_id: int = Field(alias="_progarchives_artist_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=datetime.utcnow)

    id: str
    name: str
    popularity: int = None

    genres: list[str] = []

    def dict(self, *args, **kwargs):
        _dict = super().dict(by_alias=True, *args, **kwargs) 
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict


class ArtistRef(BaseModel, extra=Extra.ignore):
    id: str
    name: str


class Album(BaseModel, extra=Extra.ignore):
    progarchives_album_id: int = Field(alias="_progarchives_album_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=datetime.utcnow)

    id: str
    name: str
    release_date: date
    release_date_precision: str
    total_tracks: int
    image_url: str = Field(alias="images", default=None)
    album_type: str = None
    artists: list[ArtistRef] = []

    @validator("image_url", pre=True)
    def parse_image_url(cls, value):
        images = value

        if not images:
            return None

        sorted_images = sorted(images, key=lambda _: _["height"] * _["width"])
        bigger_image = sorted_images[-1]

        return bigger_image["url"]

    def dict(self, *args, **kwargs):
        _dict = super().dict(by_alias=True, *args, **kwargs) 
        _dict['release_date'] = self.release_date.isoformat()
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict


class Track(BaseModel, extra=Extra.ignore):
    progarchives_album_id: int = Field(alias="_progarchives_album_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=datetime.utcnow)

    id: str
    name: str
    track_number: int = None
    disc_number: int = None
    release_date_precision: str = None
    duration_ms: int = None
    explicit: bool = None

    artists: list[ArtistRef] = []

    def dict(self, *args, **kwargs):
        _dict = super().dict(by_alias=True, *args, **kwargs) 
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict


class AudioFeature(BaseModel, extra=Extra.ignore):
    progarchives_album_id: int = Field(alias="_progarchives_album_id", default=None)
    updated_at: datetime = Field(alias="_updated_at", default_factory=datetime.utcnow)

    id: str  # Track ID
    danceability: float = None
    energy: float = None
    key: int = None
    loudness: float = None
    mode: int = None
    speechiness: float = None
    acousticness: float = None
    instrumentalness: float = None
    liveness: float = None
    valence: float = None
    tempo: float = None
    duration_ms: int = None
    time_signature: int = None
    analysis_url: str = None

    def dict(self, *args, **kwargs):
        _dict = super().dict(by_alias=True, *args, **kwargs) 
        _dict['_updated_at'] = self.updated_at.isoformat()
        return _dict
