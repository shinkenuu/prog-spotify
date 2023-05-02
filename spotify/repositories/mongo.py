from typing import Any

from pymongo import MongoClient, UpdateOne

from config import DATABASE_URI

# from spotify.repositories.decorators import ignore_dups
from spotify.models import ProgSpot
from spotify.models.spotify import Artist, Album, Track, AudioFeature

_client = MongoClient(DATABASE_URI)
_spotify_db = _client.spotify

_spotify_db.artists.create_index("id", unique=True)
_spotify_db.albums.create_index("id", unique=True)
_spotify_db.tracks.create_index("id", unique=True)
_spotify_db.audio_features.create_index("id", unique=True)

_spotify_db.prog_spot.create_index("prog_artist_id")
_spotify_db.prog_spot.create_index("prog_album_id")
_spotify_db.prog_spot.create_index("spot_artist_id")
_spotify_db.prog_spot.create_index("spot_album_id")

# ================ ARTIST ================


class MongoRepository:
    _collection = None
    _model = None

    @classmethod
    def find(cls, filter: dict[str, Any] = {}):
        documents = cls._collection.find(filter)
        validated_documents = [cls._model(**document) for document in documents]

        return validated_documents

    @classmethod
    def find_one(cls, filter: dict[str:Any]):
        document = cls._collection.find_one(filter)
        validated_document = cls._model(**document) if document else None

        return validated_document

    @classmethod
    def upsert(cls, document):
        document_json = document.dict()
        return cls._collection.replace_one(
            {"id": document_json["id"]}, document_json, upsert=True
        ).upserted_id


class ArtistMongoRepository(MongoRepository):
    _collection = _spotify_db.artists
    _model = Artist


class AlbumMongoRepository(MongoRepository):
    _collection = _spotify_db.albums
    _model = Album


class TrackMongoRepository(MongoRepository):
    _collection = _spotify_db.tracks
    _model = Track


class AudioFeatureMongoRepository(MongoRepository):
    _collection = _spotify_db.audio_features
    _model = AudioFeature


class ProgSpotMongoRepository(MongoRepository):
    _collection = _spotify_db.prog_spot
    _model = ProgSpot

    @classmethod
    def has_progarchives_artist(cls, artist_id: str | int):
        return cls._collection.count_documents({"prog_artist_id": int(artist_id)}) > 0

    @classmethod
    def has_progarchives_album(cls, album_id: str | int):
        return cls._collection.count_documents({"prog_album_id": int(album_id)}) > 0

    @classmethod
    def upsert(cls, document):
        document_dict = document.dict(exclude_unset=True)

        upsert_keys = {
            field: value
            for field, value in document_dict.items()
            if "prog" in field and value
        }

        return cls._collection.update_many(
            upsert_keys, {"$set": document_dict}, upsert=True
        ).upserted_id
    