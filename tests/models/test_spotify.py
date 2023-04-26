from spotify.models.spotify import Artist, Album, Track, AudioFeature


def test_deserialize_artist(artist_json, artist):
    # ARRANGE
    expected_artist = artist

    # ACT
    actual_artist = Artist(**artist_json)

    # ASSERT
    assert actual_artist == expected_artist


def test_deserialize_album(album_json, album):
    # ARRANGE
    expected_album = album

    # ACT
    actual_album = Album(**album_json)

    # ASSERT
    assert actual_album == expected_album


def test_deserialize_track(track_json, track):
    # ARRANGE
    expected_track = track

    # ACT
    actual_track = Track(**track_json)

    # ASSERT
    assert actual_track == expected_track


def test_deserialize_audio_features(audio_features_json, audio_features):
    # ARRANGE
    expected_audio_features = audio_features

    # ACT
    actual_audio_features = AudioFeature(**audio_features_json)

    # ASSERT
    assert actual_audio_features == expected_audio_features
