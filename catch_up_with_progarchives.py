import logging

from tqdm import tqdm

from spotify import artists, albums
from spotify.clients import SpotifyClient
from spotify.repositories.local import ProgarchiveArtistLocalRepository
from spotify.repositories.mongo import ProgSpotMongoRepository

logging.basicConfig(filename='catch_up_with_progarchives.log', filemode='a', level=logging.DEBUG)


def main():
    spotify_client = SpotifyClient()

    progarchives_artists = ProgarchiveArtistLocalRepository.read()
    logging.info(f'Total progarchives artists: {len(progarchives_artists)}')

    for progarchives_artist_id in tqdm(progarchives_artists):

        logging.debug(f'Progarchives artist {progarchives_artist_id}')

        if ProgSpotMongoRepository.has_progarchives_artist(progarchives_artist_id):
            logging.info(f'Progarchives artist already exists in mongo')
            continue

        progarchives_artist = progarchives_artists[progarchives_artist_id]
        progarchives_album_names = progarchives_artist["albums"].values()

        logging.info(f'Progarchives artist: {progarchives_artist}')

        _, *spotify_artist_albums = artists.sync(
            progarchives_artist_id=progarchives_artist_id,
            progarchives_artist_name=progarchives_artist["name"],
            progarchives_album_names=progarchives_album_names,
            spotify_client=spotify_client,
        )

        for progarchives_album_id in progarchives_artist["albums"]:
            progarchives_album_name = progarchives_artist["albums"][
                progarchives_album_id
            ]

            albums.sync(
                progarchives_artist_id=progarchives_artist_id,
                progarchives_album_id=progarchives_album_id,
                progarchives_album_name=progarchives_album_name,
                spotify_albums=spotify_artist_albums,
            )


if __name__ == "__main__":
    main()
