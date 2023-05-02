from os import getenv

SPOTIPY_CLIENT_ID = getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = getenv("SPOTIPY_CLIENT_SECRET")

DATABASE_URI = getenv(
    "DATABASE_URI",
    "mongodb://root:leaf@127.0.0.1:27018/spotify?authSource=admin&authMechanism=SCRAM-SHA-256",
)

PAGINATION_INTERVAL_SECONDS = int(getenv("SLEEP_SECONDS", "3"))
MIN_SECONDS_BETWEEN_REQUESTS = int(getenv("MIN_SECONDS_BETWEEN_REQUESTS", "3"))