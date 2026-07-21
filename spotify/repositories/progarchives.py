"""Read-only repositories for the ProgArchives PostgreSQL database."""

from typing import Any, Generator

import psycopg

from config import settings


class ProgArchivesDB:
    """Singleton that lazily creates a ProgArchives PostgreSQL connection."""

    _instance: "ProgArchivesDB | None" = None

    def __new__(cls) -> "ProgArchivesDB":
        if cls._instance:
            return cls._instance

        cls._instance = super().__new__(cls)
        cls._instance._conn = psycopg.connect(settings.PROGARCHIVES_DATABASE_URL)
        cls._instance._conn.autocommit = True

        return cls._instance

    _conn: Any

    @property
    def connection(self):
        return self._conn


class ProgArchivesArtistRepository:
    """Read ProgArchives artists (with albums) from PostgreSQL."""

    @classmethod
    def count_all(cls) -> int:
        """Return total number of artists."""
        conn = ProgArchivesDB().connection
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM artists")
            return cur.fetchone()[0]

    @classmethod
    def iter_all(cls) -> Generator[tuple[str, dict], None, None]:
        """Yield (artist_id, artist_data) one at a time.

        Each yielded item:
            ("1", {"name": "GENESIS", "albums": {"2": "FOXTROT", ...}})
        """
        conn = ProgArchivesDB().connection
        with conn.cursor(name="artist_stream", withhold=True) as cur:
            cur.execute("""
                SELECT a.id, a.name
                FROM artists a
                ORDER BY a.id
            """)
            cur.itersize = 100

            for artist_id, artist_name in cur:
                aid = str(artist_id)
                artist_data: dict = {"name": artist_name, "albums": {}}

                with conn.cursor() as inner_cur:
                    inner_cur.execute(
                        "SELECT id, name FROM albums WHERE artist_id = %s ORDER BY id",
                        (artist_id,),
                    )
                    for alb_id, alb_name in inner_cur:
                        artist_data["albums"][str(alb_id)] = alb_name

                yield aid, artist_data

    @classmethod
    def find_one(cls, artist_id: str | int) -> dict | None:
        """Return a single artist by id, or None if not found."""
        conn = ProgArchivesDB().connection
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name FROM artists WHERE id = %s",
                (int(artist_id),),
            )
            row = cur.fetchone()
            if not row:
                return None

            cur.execute(
                "SELECT id, name FROM albums WHERE artist_id = %s ORDER BY id",
                (int(artist_id),),
            )
            albums = {str(alb_id): alb_name for alb_id, alb_name in cur.fetchall()}

            return {"name": row[1], "albums": albums}


class ProgArchivesAlbumRepository:
    """Read ProgArchives albums grouped by artist from PostgreSQL."""

    @classmethod
    def iter_all(cls) -> Generator[tuple[str, dict[str, str]], None, None]:
        """Yield (artist_id, albums_dict) grouped by artist.

        Each yielded item:
            ("1", {"2": "FOXTROT", "3": "NURSERY CRYME", ...})

        Uses server-side cursor to stream albums and buffers per-artist.
        """
        conn = ProgArchivesDB().connection
        with conn.cursor(name="album_stream", withhold=True) as cur:
            cur.execute("""
                SELECT al.artist_id, al.id, al.name
                FROM albums al
                ORDER BY al.artist_id, al.id
            """)
            cur.itersize = 500

            current_artist_id: str | None = None
            albums_dict: dict[str, str] = {}

            for artist_id, album_id, album_name in cur:
                aid = str(artist_id)
                if aid != current_artist_id:
                    if current_artist_id is not None:
                        yield current_artist_id, albums_dict
                    current_artist_id = aid
                    albums_dict = {}
                albums_dict[str(album_id)] = album_name

            if current_artist_id is not None:
                yield current_artist_id, albums_dict
