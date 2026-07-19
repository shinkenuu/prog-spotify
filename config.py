from os import getenv

SPOTIPY_CLIENT_ID = getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = getenv("SPOTIPY_CLIENT_SECRET")

SPOTIFY_DATABASE_URI = getenv(
    "SPOTIFY_DATABASE_URI",
    "mongodb://root:leaf@127.0.0.1:27018/spotify?authSource=admin&authMechanism=SCRAM-SHA-256",
)

PROGARCHIVES_DATABASE_URL = getenv(
    "PROGARCHIVES_DATABASE_URL",
    "postgresql://prog:prog@127.0.0.1:5432/progarchives?options=-c%20default_transaction_read_only=on",
)

PAGINATION_INTERVAL_SECONDS = int(getenv("SLEEP_SECONDS", "3"))
MIN_SECONDS_BETWEEN_REQUESTS = int(getenv("MIN_SECONDS_BETWEEN_REQUESTS", "3"))
