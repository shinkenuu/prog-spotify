from typing import Any, Type

from pydantic import BaseModel
from pymongo import MongoClient

from config import SPOTIFY_DATABASE_URI

# from spotify.repositories.decorators import ignore_dups
from spotify.models import ProgSpot
from spotify.models.spotify import Artist, Album, Track, AudioFeature


class MongoDB:
    """Singleton that lazily creates the MongoDB connection and indexes."""

    _instance: "MongoDB | None" = None

    def __new__(cls) -> "MongoDB":
        if cls._instance:
            return cls._instance
        
        cls._instance = super().__new__(cls)
        cls._instance._client = MongoClient(SPOTIFY_DATABASE_URI)
        cls._instance._db = cls._instance._client.spotify
        cls._instance._create_indexes()

        return cls._instance

    _client: MongoClient
    _db: Any

    def _create_indexes(self) -> None:
        self._db.artists.create_index("id", unique=True)
        self._db.albums.create_index("id", unique=True)
        self._db.tracks.create_index("id", unique=True)
        self._db.audio_features.create_index("id", unique=True)

        self._db.prog_spot.create_index("prog_artist_id")
        self._db.prog_spot.create_index("prog_album_id")
        self._db.prog_spot.create_index("spot_artist_id")
        self._db.prog_spot.create_index("spot_album_id")


class MongoRepository:
    _collection_name: str
    _model: Type[BaseModel]

    @classmethod
    def _get_collection(cls):
        return MongoDB()._db[cls._collection_name]

    @classmethod
    def find(cls, filter: dict[str, Any] = {}) -> list[BaseModel]:
        collection = cls._get_collection()
        documents = collection.find(filter)
        validated_documents = [cls._model.model_validate(document) for document in documents]

        return validated_documents

    @classmethod
    def find_one(cls, filter: dict[str, Any]) -> BaseModel | None:
        collection = cls._get_collection()
        document = collection.find_one(filter)
        validated_document = cls._model.model_validate(document) if document else None

        return validated_document

    @classmethod
    def upsert(cls, document):
        collection = cls._get_collection()
        document_json = document.model_dump(by_alias=True, mode="json")
        return collection.replace_one(
            {"id": document_json["id"]}, document_json, upsert=True
        ).upserted_id


class ArtistMongoRepository(MongoRepository):
    _collection_name = "artists"
    _model = Artist


class AlbumMongoRepository(MongoRepository):
    _collection_name = "albums"
    _model = Album


class TrackMongoRepository(MongoRepository):
    _collection_name = "tracks"
    _model = Track


class AudioFeatureMongoRepository(MongoRepository):
    _collection_name = "audio_features"
    _model = AudioFeature


# ---------------------------------------------------------------------------
# Convenience helpers used by tracks / audio_features workflows
# ---------------------------------------------------------------------------

def find_prog_spot_albums() -> list[dict]:
    """Find ProgSpot docs that have both prog_album_id and spot_album_id."""
    collection = MongoDB()._db.prog_spot
    return list(
        collection.find(
            {"prog_album_id": {"$ne": None}, "spot_album_id": {"$ne": None}},
            {"prog_album_id": 1, "spot_album_id": 1},
        )
    )


def find_tracks() -> list[dict]:
    """Find all tracks."""
    collection = MongoDB()._db.tracks
    return list(collection.find({}, {"id": 1}))


def upsert_track(track_dict: dict) -> None:
    """Upsert a single track document."""
    collection = MongoDB()._db.tracks
    collection.replace_one({"id": track_dict["id"]}, track_dict, upsert=True)


def insert_audio_features(features: list[dict]) -> None:
    """Insert audio feature documents (skips duplicates)."""
    collection = MongoDB()._db.audio_features
    if not features:
        return
    for feature in features:
        collection.replace_one({"id": feature["id"]}, feature, upsert=True)


class ProgSpotMongoRepository(MongoRepository):
    _collection_name = "prog_spot"
    _model = ProgSpot

    @classmethod
    def has_progarchives_artist(cls, artist_id: str | int) -> bool:
        collection = cls._get_collection()
        prog_artist_id = int(artist_id) if isinstance(artist_id, str) else artist_id
        return collection.count_documents({"prog_artist_id": prog_artist_id}) > 0

    @classmethod
    def has_progarchives_album(cls, album_id: str | int) -> bool:
        collection = cls._get_collection()
        album_id_ = int(album_id) if isinstance(album_id, str) else album_id
        return collection.count_documents({"prog_album_id": album_id_}) > 0

    @classmethod
    def upsert(cls, document):
        collection = cls._get_collection()
        document_dict = document.model_dump(exclude_unset=True, by_alias=True)

        upsert_keys = {
            field: value
            for field, value in document_dict.items()
            if "prog" in field and value
        }

        return collection.update_many(
            upsert_keys, {"$set": document_dict}, upsert=True
        ).upserted_id
    