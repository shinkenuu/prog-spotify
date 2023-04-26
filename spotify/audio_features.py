from tqdm import tqdm
from time import sleep

from spotify.repositories.local import read_visited, write_visited
from spotify.repositories.mongo import find_tracks, insert_audio_features
from spotify.clients import SpotifyClient


MAX_TRACK_IDS_PER_REQUEST = 100


def main():
    spotify = SpotifyClient()

    visited = read_visited()
    track_ids = [track["id"] for track in find_tracks()]
    track_ids.sort()

    chunks = len(track_ids) // MAX_TRACK_IDS_PER_REQUEST

    try:
        for chunk_index in tqdm(range(chunks)):
            if str(chunk_index) in visited:
                continue

            chunk_start = chunk_index * MAX_TRACK_IDS_PER_REQUEST
            chunk_end = chunk_start + MAX_TRACK_IDS_PER_REQUEST

            chunk_track_ids = track_ids[chunk_start:chunk_end]

            sleep(1)
            audio_features = spotify.audio_features(chunk_track_ids)
            visited.add(str(chunk_index))

            insert_audio_features(audio_features)

        chunk_track_ids = track_ids[chunk_end:]
        audio_features = spotify.audio_features(chunk_track_ids)
        insert_audio_features(audio_features)

    except (Exception, KeyboardInterrupt) as error:
        print(error)

    write_visited(visited)
