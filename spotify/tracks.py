from tqdm import tqdm
from time import sleep

from spotify.repositories.local import read_visited, write_visited
from spotify.repositories.mongo import find_prog_spot_albums, upsert_track
from spotify.clients import SpotifyClient


def main():
    spotify = SpotifyClient()

    visited = read_visited()
    progspot_albums = list(find_prog_spot_albums())
    progspot_albums.sort(key=lambda x: x["spotify_id"])

    try:
        for progspot_album in tqdm(progspot_albums):
            spotify_album_id = progspot_album["spotify_id"]

            if spotify_album_id in visited:
                continue

            sleep(1)
            album_tracks = spotify.album_tracks(spotify_album_id)
            visited.add(spotify_album_id)

            # insert_tracks(album_tracks)
            for album_track in album_tracks:
                album_track["_album_id"] = spotify_album_id
                upsert_track(album_track)

    except (Exception, KeyboardInterrupt) as error:
        print(error)

    write_visited(visited)
