from spotify.models.spotify import Artist, Album, Track, AudioFeature


def _compare_without_updated_at(actual, expected):
    actual_dict = actual.dict()
    actual_dict.pop("_updated_at")

    expected_dict = expected.dict()
    expected_dict.pop("_updated_at")

    assert actual_dict == expected_dict


def test_deserialize_artist(artist_json, artist):
    # ARRANGE
    expected_artist = artist

    # ACT
    actual_artist = Artist(**artist_json)

    # ASSERT
    _compare_without_updated_at(actual_artist, expected_artist)


def test_deserialize_album(album_json, album):
    # ARRANGE
    expected_album = album

    # ACT
    actual_album = Album(**album_json)

    # ASSERT
    _compare_without_updated_at(actual_album, expected_album)


def test_deserialize_album_with_release_date_containing_just_year(album_json, album):
    # ARRANGE
    expected_album = album
    expected_album.release_date = None

    album_json['release_date'] = '1970'

    # ACT
    actual_album = Album(**album_json)

    # ASSERT
    _compare_without_updated_at(actual_album, expected_album)


def test_deserialize_album_with_release_date_containing_just_year_and_month(
    album_json, album
):
    # ARRANGE
    expected_album = album
    expected_album.release_date = None

    album_json['release_date'] = '1970-10'

    # ACT
    actual_album = Album(**album_json)

    # ASSERT
    _compare_without_updated_at(actual_album, expected_album)


def test_deserialize_track(track_json, track):
    # ARRANGE
    expected_track = track

    # ACT
    actual_track = Track(**track_json)

    # ASSERT
    _compare_without_updated_at(actual_track, expected_track)


def test_deserialize_audio_features(audio_features_json, audio_features):
    # ARRANGE
    expected_audio_features = audio_features

    # ACT
    actual_audio_features = AudioFeature(**audio_features_json)

    # ASSERT
    _compare_without_updated_at(actual_audio_features, expected_audio_features)
