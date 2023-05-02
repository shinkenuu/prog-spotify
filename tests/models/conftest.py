import json
from datetime import datetime

from pytest import fixture

from spotify.models.spotify import Artist, Album, ArtistRef, Track, AudioFeature


# ===================================================
# ====================== ARTIST =====================
# ===================================================


@fixture
def artist_json():
    with open("./tests/fixtures/artist.json") as file:
        return json.load(file)


@fixture
def artist():
    artist = Artist(
        id="3CkvROUTQ6nRi9yQOcsB50",
        name="Genesis",
        popularity=71,
        genres=[
            "album rock",
            "art rock",
            "classic rock",
            "mellow gold",
            "progressive rock",
            "rock",
            "soft rock",
            "symphonic rock",
        ],
    )

    return artist


# ===================================================
# ====================== ALBUM ======================
# ===================================================


@fixture
def album_json():
    with open("./tests/fixtures/album.json") as file:
        return json.load(file)


@fixture
def album():
    album = Album(
        id="3y67YB3vSbaopIg1VoAO1n",
        name="Foxtrot",
        release_date='1972-10-06',
        release_date_precision="day",
        total_tracks=6,
        album_type="album",
        artists=[
            ArtistRef(
                id="3CkvROUTQ6nRi9yQOcsB50",
                name="Genesis",
            )
        ],
    )

    album.image_url = "https://i.scdn.co/image/ab67616d0000b27369337b6f76bd7943acdcd192"
    return album


# ===================================================
# ====================== TRACK ======================
# ===================================================


@fixture
def track_json():
    with open("./tests/fixtures/track.json") as file:
        return json.load(file)


@fixture
def track():
    track = Track(
        id="7MoGxkj89GJrWtH6WUlHeT",
        name="Too Much Sugar",
        disc_number=1,
        duration_ms=213000,
        explicit=False,
        track_number=2,
        artists=[
            ArtistRef(
                id="0ESuAaigvHag23HHvbelX9",
                name="Phaedra",
            )
        ],
    )

    return track


# ===================================================
# =============== AUDIO FEATURES ====================
# ===================================================


@fixture
def audio_features_json():
    with open("./tests/fixtures/audio_features.json") as file:
        return json.load(file)


@fixture
def audio_features():
    audio_feature = AudioFeature(
        id="3jMjzmmLk3TqAwkDkkOZFW",
        danceability=0.346,
        energy=0.141,
        key=2,
        loudness=-12.581,
        mode=0,
        speechiness=0.0393,
        acousticness=0.542,
        instrumentalness=0.00507,
        liveness=0.103,
        valence=0.0381,
        tempo=122.028,
        duration_ms=721920,
        time_signature=3,
        analysis_url="https://api.spotify.com/v1/audio-analysis/3jMjzmmLk3TqAwkDkkOZFW",
    )

    return audio_feature
