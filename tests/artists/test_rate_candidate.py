from spotify.artists import _rate_candidate


def test_rates_the_desired_higher_than_undesired_artist(
    genesis_bundle, genesis_candidates_bundles
):
    # ARRANGE

    # ACT
    genesis_rate = _rate_candidate(
        progarchives_artist_name=genesis_bundle["prog"]["artist"]["name"],
        progarchives_album_names=genesis_bundle["prog"]["albums"],
        spotify_artist_name=genesis_bundle["spot"]["artist"].name,
        spotify_albums=genesis_bundle["spot"]["albums"],
    )

    candidates_rates = [
        _rate_candidate(
            progarchives_artist_name=genesis_candidate_bundle["prog"]["artist"]["name"],
            progarchives_album_names=genesis_candidate_bundle["prog"]["albums"],
            spotify_artist_name=genesis_candidate_bundle["spot"]["artist"].name,
            spotify_albums=genesis_candidate_bundle["spot"]["albums"],
        )
        for genesis_candidate_bundle in genesis_candidates_bundles
    ]

    # ASSERT
    max_candidate_rate = max(candidates_rates)
    assert genesis_rate > max_candidate_rate
