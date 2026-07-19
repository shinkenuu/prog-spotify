import json
from pathlib import Path
from typing import Iterable

from spotify.models import spotify as spotify_models


_VISITED_PATH = Path("./storage/.visited")


def read_visited(path: Path = _VISITED_PATH) -> set:
    """Read a set of visited IDs from a JSON file."""
    if not path.exists():
        return set()
    with open(path) as f:
        return set(json.load(f))


def write_visited(visited: set, path: Path = _VISITED_PATH) -> None:
    """Write a set of visited IDs to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(list(visited), f)

class JsonReadMixin:
    _path: str
    _model: type

    @classmethod
    def read(cls, path: str = None):
        path = path or cls._path

        with open(path) as file:
            file_content = json.load(file)

        content = (
            [cls._model(**item) for item in file_content]
            if cls._model
            else file_content
        )

        return content


class JsonWriteMixin:
    _path: str
    _model: type

    @classmethod
    def write(cls, content: Iterable, path: str = None):
        path = path or cls._path

        writable = [item.model_dump(by_alias=True) for item in content] if cls._model else content

        with open(path, "w") as file:
            return json.dump(writable, file)


class TextLineReadMixin:
    _path: str

    @classmethod
    def read(cls, path: str = None):
        path = path or cls._path

        with open(path) as file:
            return {line.strip() for line in file.readlines()}


class TextLineWriteMixin:
    _path: str

    @classmethod
    def write(cls, content: Iterable, path: str = None):
        path = path or cls._path

        with open(path, "a") as file:
            return file.write("\n".join(content))


# ==========================================================
# ====================== SPOTIFY ===========================
# ==========================================================


class ArtistLocalRepository(JsonReadMixin, JsonWriteMixin):
    _path = "./storage/artist.json"
    _model = spotify_models.Artist


class AlbumLocalRepository(JsonReadMixin, JsonWriteMixin):
    _path = "./storage/album.json"
    _model = spotify_models.Album


class TrackLocalRepository(JsonReadMixin, JsonWriteMixin):
    _path = "./storage/track.json"
    _model = spotify_models.Track


class AudioFeatureLocalRepository(JsonReadMixin, JsonWriteMixin):
    _path = "./storage/audio_feature.json"
    _model = spotify_models.AudioFeature


# ==========================================================
# ==================== PROGARCHIVES ========================
# ==========================================================


class ProgarchiveArtistLocalRepository(JsonReadMixin, JsonWriteMixin):
    _path = "./storage/_progarchives_artists.json"
    _model = None


class ProgarchiveAlbumLocalRepository(JsonReadMixin, JsonWriteMixin):
    _path = "./storage/_progarchives_albums.json"
    _model = None


class ProgarchiveOnlyArtistLocalRepository(TextLineReadMixin, TextLineWriteMixin):
    _path = "./storage/_progarchives_only_artists.json"


class ProgarchiveOnlyAlbumLocalRepository(TextLineReadMixin, TextLineWriteMixin):
    _path = "./storage/_progarchives_only_albums.json"
