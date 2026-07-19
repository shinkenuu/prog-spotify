# AGENTS.md — ProgSpot

## What This Project Does

Matches **ProgArchives** artists and albums with **Spotify** equivalents using fuzzy string matching, then stores the relationships in MongoDB.

**Core workflow:**
1. Read ProgArchives artist/album data from local JSON files (`./storage/_progarchives_*.json`)
2. Search Spotify API for matching artists using `thefuzz` (fuzzy string matching)
3. Rate candidates by artist name similarity + album name overlap
4. Store ProgArchives ↔ Spotify mappings in MongoDB `prog_spot` collection
5. Fetch full Spotify data (albums, tracks, audio features) for matched items

## Tech Stack

- **Python 3.13** — managed by **uv**
- **spotipy** — Spotify Web API client
- **pymongo** — MongoDB driver
- **pydantic** (v1.x style with `extra="ignore"`) — data models
- **thefuzz** + **python-levenshtein** — fuzzy string matching
- **pytest** — testing
- **ruff** — linting (via `uv tool run ruff`)
- **MongoDB 8.3** — via Docker Compose

## Project Structure

```
spotify/
├── catch_up_with_progarchives.py  # Main entry: iterate all ProgArchives artists, match + sync
├── refresh.py                     # Refresh a single ProgArchives artist by ID
├── fetch.py                       # CLI exploration: search artist/album, fetch albums
├── config.py                      # Env vars: Spotify credentials, DB URI, rate limits
├── docker-compose.yaml            # MongoDB 8.3 on port 27018
├── Makefile                       # test, lint, clean targets
├── pyproject.toml                 # uv project config + dependencies
│
├── spotify/                       # Main package
│   ├── clients.py                 # SpotifyClient: rate-limited wrapper around spotipy
│   ├── artists.py                 # Artist matching logic + sync
│   ├── albums.py                  # Album matching logic + sync
│   ├── tracks.py                  # Fetch tracks for matched albums
│   ├── audio_features.py          # Fetch audio features for tracks (batched, 100/request)
│   ├── models/
│   │   ├── progarchives.py        # ProgArchives Artist model (name + albums dict)
│   │   └── spotify.py             # Spotify models: Artist, Album, Track, AudioFeature
│   └── repositories/
│       ├── local.py               # JSON file read/writes for ProgArchives data + visited tracking
│       ├── mongo.py               # MongoDB singleton + repo classes for all models
│       └── decorators.py          # @ignore_dups decorator for BulkWriteError
│
├── tests/
│   ├── models/test_spotify.py     # Model deserialization tests
│   ├── albums/                    # Album matching tests
│   └── artists/                   # Artist rating tests
│
└── storage/                       # Local JSON data (gitignored)
    ├── _progarchives_artists.json  # {artist_id: {name, albums: {album_id: name}}}
    ├── _progarchives_albums.json   # {artist_id: {album_id: name}}
    └── ...                        # Other ProgArchives exports + visited tracking
```

## Key Concepts

### Matching Algorithm (`spotify/artists.py`)

1. **Search** Spotify for artist by name → get candidates
2. **Pre-rate** by name similarity alone (threshold 90) — avoids wasting API calls
3. **Full rate** by name + album overlap: `1 * artist_score + 3 * avg_album_scores`
4. Thresholds: pre-rate ≥ 90, full-rate ≥ 100, early-exit at ≥ 250

### Album Matching (`spotify/albums.py`)

Uses `thefuzz.process.extractOne` with threshold 90 to match ProgArchives album names against Spotify artist's albums.

### Rate Limiting

- `MIN_SECONDS_BETWEEN_REQUESTS` (default 3s) between API calls
- `PAGINATION_INTERVAL_SECONDS` (default 3s) between paginated pages
- Max 5 pages per paginated request

### MongoDB Collections

| Collection       | Unique Index | Purpose                              |
|-----------------|-------------|--------------------------------------|
| `artists`       | `id`        | Spotify artists with progarchives_id |
| `albums`        | `id`        | Spotify albums with progarchives_id  |
| `tracks`        | `id`        | Spotify tracks                       |
| `audio_features`| `id`        | Audio features per track             |
| `prog_spot`     | none        | Mapping: prog_artist_id ↔ spot_artist_id, prog_album_id ↔ spot_album_id |

### `ProgSpot` Model

Linking table that stores partial or complete mappings:
- `{prog_artist_id: 1, spot_artist_id: "3CkvROUTQ6nRi9yQOcsB50"}` — artist matched
- `{prog_artist_id: 1, prog_album_id: 2, spot_album_id: "3y67YB3vSbaopIg1VoAO1n"}` — album matched

Upserted by ProgArchives ID (not Spotify ID), so unmatched items still get a doc with `None` for the Spotify side.

## Running the Project

```bash
# Start MongoDB
docker compose up -d mongo

# Run tests
make test          # uv run pytest ./tests -vv

# Lint
make lint          # uv tool run ruff check . --fix

# Full sync (all ProgArchives artists)
source .env && uv run python catch_up_with_progarchives.py

# Refresh single artist
source .env && ARTIST_ID=214 uv run python refresh.py

# CLI exploration
source .env && ARTIST_NAME="Genesis" uv run python fetch.py
```

## Test Fixtures

- `tests/fixtures/` — JSON files for model deserialization tests
- `tests/fixtures/progarchives_artists/` — Per-artist JSON for rating tests
- `tests/fixtures/spotify_artists/` — Spotify artist JSON
- `tests/fixtures/spotify_albums/` — Spotify album arrays per artist
- `tests/fixtures/__init__.py` — `@lru_cache`-decorated loaders
- `tests/albums/fixtures.py` — Hand-crafted fixtures for album matching tests

## Common Patterns

- **Pydantic models** tolerates extra Spotify API fields
- **MongoDB models** have `.dict()` that serializes with `by_alias=True` and ISO-formatted dates
- **Repositories** follow a class-based pattern: `ArtistMongoRepository.upsert(doc)`, `ArtistMongoRepository.find_one(filter)`
- **Visited tracking** uses `read_visited()` / `write_visited()` in `local.py` for resumable batch operations
- **Entry points** (`catch_up_with_progarchives.py`, `tracks.py`, `audio_features.py`) have `main()` + `if __name__ == "__main__"` guards
