from spotify.models.spotify import Album, ArtistRef


lunar_chateau_progarchives_albums = {
    822: "LUNAR CHATEAU",
    823: "BEYOND THE REACH OF DREAMS",
}


lunar_chateau_spotify_albums = [
    Album(
        _progarchives_album_id=823,
        id="1aCWNHMMGXSQuBl9JCP6iT",
        name="Beyond The Reach Of Dreams",
        release_date="2010-01-26",
        release_date_precision="day",
        total_tracks=6,
        album_type="album",
        artists=[ArtistRef(id="3t2LVPsyc5UgrCN1WtXORD", name="Lunar Chateau")],
    ),
    Album(
        _progarchives_album_id=822,
        id="5TlW8DnerymmHPpQ10cQMK",
        name="Lunar Chateau",
        release_date="2009-12-01",
        release_date_precision="day",
        total_tracks=12,
        album_type="album",
        artists=[ArtistRef(id="3t2LVPsyc5UgrCN1WtXORD", name="Lunar Chateau")],
    ),
]


def find_match(progarchives_album_id, spotify_albums):
    for album in spotify_albums:
        if album.progarchives_album_id == progarchives_album_id:
            return album
