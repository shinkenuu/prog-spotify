from os import getenv

SPOTIPY_CLIENT_ID = getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = getenv("SPOTIPY_CLIENT_SECRET")

DATABASE_URI = getenv(
    "DATABASE_URI",
    "mongodb://root:leaf@127.0.0.1:27017/spotify?authSource=admin&authMechanism=SCRAM-SHA-256",
)
