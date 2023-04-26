from spotify.models.spotify import Artist, Album, ArtistRef

from pytest import fixture


@fixture
def genesis_bundle():
    prog = {
        "artist": {
            "id": "1",
            "name": "GENESIS",
        },
        "albums": [
            "FOXTROT",
            "NURSERY CRYME",
            "A TRICK OF THE TAIL",
            "FROM GENESIS TO REVELATION",
            "SELLING ENGLAND BY THE POUND",
            "THE LAMB LIES DOWN ON BROADWAY",
            "WIND & WUTHERING",
            "...AND THEN THERE WERE THREE...",
            "DUKE",
            "ABACAB",
            "GENESIS",
            "INVISIBLE TOUCH",
            "WE CAN'T DANCE",
            "CALLING ALL STATIONS",
            "TRESPASS",
        ],
    }
    spot = {
        "artist": Artist(
            id="3CkvROUTQ6nRi9yQOcsB50",
            name="Genesis",
            popularity=69,
            genres=[
                "album rock",
                "art rock",
                "classic rock",
                "hard rock",
                "mellow gold",
                "progressive rock",
                "rock",
                "soft rock",
                "symphonic rock",
            ],
        ),
        "albums": [
            Album(
                id="2VMk6eFV1MafApI6Txke5H",
                name="The Last Domino?",
                release_date="2021-11-19",
                release_date_precision="day",
                total_tracks=27,
                image_url="https://i.scdn.co/image/ab67616d0000b2733c21170f4571818d67f7934e",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="2Khy2ibPothF9h62okhICI",
                name="Live - The Way We Walk, Volume Two: The Longs",
                release_date="1993-01-11",
                release_date_precision="day",
                total_tracks=6,
                image_url="https://i.scdn.co/image/ab67616d0000b27399a196101852365470e0f5f3",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="25tGlHylelmscMQjEqFn5F",
                name="Live - The Way We Walk, Volume One: The Shorts",
                release_date="1992-11-16",
                release_date_precision="day",
                total_tracks=11,
                image_url="https://i.scdn.co/image/ab67616d0000b2737f63092692060790d18c2ee2",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="4Oao6gCD44a9vSruFH7F33",
                name="According to Phil Collins",
                release_date="1988-07-25",
                release_date_precision="day",
                total_tracks=16,
                image_url="https://i.scdn.co/image/ab67616d0000b2739674e8576b02a7d9fed852ad",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="5BDGtXKMQ6k267KX4PoGhP",
                name="Invisible Touch",
                release_date="1986-06-09",
                release_date_precision="day",
                total_tracks=8,
                image_url="https://i.scdn.co/image/ab67616d0000b273087ca24aa58e7c67514061a1",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="6BX8AS7J97PSQNrteX325Z",
                name="Genesis",
                release_date="1983-10-03",
                release_date_precision="day",
                total_tracks=9,
                image_url="https://i.scdn.co/image/ab67616d0000b273945c366eda66495226e4a46d",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="4B84Q4vYuoTPaxmFMYlbWD",
                name="A Trick of the Tail (2007 Remaster)",
                release_date="1976-02-02",
                release_date_precision="day",
                total_tracks=8,
                image_url="https://i.scdn.co/image/ab67616d0000b27358dccdc06dafe0d0dc170283",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="2tSRe2rkdJvZWMOIZpu6lk",
                name="Selling England By The Pound",
                release_date="1973-10-12",
                release_date_precision="day",
                total_tracks=8,
                image_url="https://i.scdn.co/image/ab67616d0000b273769a32367e8bb631560572fd",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="0OJK0Hst2fUzpRj5Dy1yxQ",
                name="Live",
                release_date="1973-07-20",
                release_date_precision="day",
                total_tracks=5,
                image_url="https://i.scdn.co/image/ab67616d0000b27347c6a140256b244e29637e3f",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="1FcTAH4sBWvtdO55OffwCQ",
                name="Nursery Cryme",
                release_date="1971-11-12",
                release_date_precision="day",
                total_tracks=7,
                image_url="https://i.scdn.co/image/ab67616d0000b273b33e0bfac977a389d5db7dc6",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="0mKr6PDMuhTEWatlw5a4hl",
                name="Trespass",
                release_date="1970-10-23",
                release_date_precision="day",
                total_tracks=6,
                image_url="https://i.scdn.co/image/ab67616d0000b2731fcab41c48d68a34f5c19486",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
            Album(
                id="7ykLKrLtN920GC9SBKhpp9",
                name="From Genesis to Revelation",
                release_date="1969-03-17",
                release_date_precision="day",
                total_tracks=21,
                image_url="https://i.scdn.co/image/ab67616d0000b2732262b373042561b144249d3e",
                album_type="album",
                artists=[ArtistRef(id="3CkvROUTQ6nRi9yQOcsB50", name="Genesis")],
            ),
        ],
    }

    return {"prog": prog, "spot": spot}


@fixture
def genesis_candidates_bundles(
    genesis_bundle,
    genesis_candidate_6vHBuUxrcpn1do5UaEJ7g6_spot_bundle,
    genesis_candidate_1i0FwIJ3oUPrLSVrDXZfrt_spot_bundle,
    genesis_candidate_1YWaABizGll91McSy7RLzg_spot_bundle,
):
    genesis_prog_bundle = genesis_bundle["prog"]
    bundles = [
        {
            "prog": genesis_prog_bundle,
            "spot": genesis_candidate_spot_bundle,
        }
        for genesis_candidate_spot_bundle in [
            genesis_candidate_6vHBuUxrcpn1do5UaEJ7g6_spot_bundle,
            genesis_candidate_1i0FwIJ3oUPrLSVrDXZfrt_spot_bundle,
            genesis_candidate_1YWaABizGll91McSy7RLzg_spot_bundle,
        ]
    ]

    return bundles


@fixture
def genesis_candidate_6vHBuUxrcpn1do5UaEJ7g6_spot_bundle():
    return {
        "artist": Artist(
            id="6vHBuUxrcpn1do5UaEJ7g6",
            name="Domo Genesis",
            popularity=60,
            genres=["alternative hip hop", "underground hip hop"],
        ),
        "albums": [
            Album(
                id="3GncI0ExXYyWnIzZe9oxRQ",
                name="No Idols",
                release_date="2023-04-20",
                release_date_precision="day",
                total_tracks=12,
                image_url="https://i.scdn.co/image/ab67616d0000b2733bb6cd42ce92bead1110b09d",
                album_type="album",
                artists=[
                    ArtistRef(id="6vHBuUxrcpn1do5UaEJ7g6", name="Domo Genesis"),
                    ArtistRef(id="0eVyjRhzZKke2KFYTcDkeu", name="The Alchemist"),
                ],
            ),
            Album(
                id="6EPg4n0tIsQpXmfAnpLHzq",
                name="Intros, Outros & Interludes",
                release_date="2022-07-29",
                release_date_precision="day",
                total_tracks=11,
                image_url="https://i.scdn.co/image/ab67616d0000b273335355b3708b6f7a28b49fe2",
                album_type="album",
                artists=[ArtistRef(id="6vHBuUxrcpn1do5UaEJ7g6", name="Domo Genesis")],
            ),
            Album(
                id="3dESO7Q9gmDkYn2Y8Yrupy",
                name="Arent U Glad Youre U",
                release_date="2018-01-19",
                release_date_precision="day",
                total_tracks=8,
                image_url="https://i.scdn.co/image/ab67616d0000b2731a125b32ff6cc73517d22344",
                album_type="album",
                artists=[ArtistRef(id="6vHBuUxrcpn1do5UaEJ7g6", name="Domo Genesis")],
            ),
            Album(
                id="6h6GbuoVE9hQiriHFV71Vx",
                name="Purple Corolla",
                release_date="2017-09-15",
                release_date_precision="day",
                total_tracks=10,
                image_url="https://i.scdn.co/image/ab67616d0000b2737f93fceb1eccc0a396d64f3e",
                album_type="album",
                artists=[ArtistRef(id="6vHBuUxrcpn1do5UaEJ7g6", name="Domo Genesis")],
            ),
            Album(
                id="6hcTis2h9nAjTVHKfg9kbR",
                name="Genesis (Japan Version)",
                release_date="2016-07-06",
                release_date_precision="day",
                total_tracks=13,
                image_url="https://i.scdn.co/image/ab67616d0000b273ff965bee6682de920eb1ce04",
                album_type="album",
                artists=[ArtistRef(id="6vHBuUxrcpn1do5UaEJ7g6", name="Domo Genesis")],
            ),
            Album(
                id="3mhZHDmHvIUAeAYH7MrXBW",
                name="Genesis",
                release_date="2016-03-25",
                release_date_precision="day",
                total_tracks=12,
                image_url="https://i.scdn.co/image/ab67616d0000b273085d6629aaaf7baa283d5c7d",
                album_type="album",
                artists=[ArtistRef(id="6vHBuUxrcpn1do5UaEJ7g6", name="Domo Genesis")],
            ),
        ],
    }


@fixture
def genesis_candidate_1i0FwIJ3oUPrLSVrDXZfrt_spot_bundle():
    return {
        "artist": Artist(
            id="1i0FwIJ3oUPrLSVrDXZfrt", name="New Genesis", popularity=3, genres=[]
        ),
        "albums": [],
    }


@fixture
def genesis_candidate_1YWaABizGll91McSy7RLzg_spot_bundle():
    return {
        "artist": Artist(
            id="1YWaABizGll91McSy7RLzg", name="genesis555", popularity=11, genres=[]
        ),
        "albums": [
            Album(
                id="1COjciJhyCQXbcaubh0A60",
                name="genesis chapter 1",
                release_date="2022-06-10",
                release_date_precision="day",
                total_tracks=17,
                image_url="https://i.scdn.co/image/ab67616d0000b273a8f7acde2d3205d2c23741ab",
                album_type="album",
                artists=[ArtistRef(id="1YWaABizGll91McSy7RLzg", name="genesis555")],
            )
        ],
    }


# =========================================================
# =========================================================
# =========================================================


@fixture
def advent_bundle():
    bundle = {
        "prog": {
            "artist": {
                "id": 123,
                "name": "ADVENT",
            },
            "albums": ["ADVENT", "CANTUS FIRMUS", "SILENT SENTINEL"],
        },
        "spot": {"artist": None, "albums": []},
    }

    return bundle


@fixture
def advent_candidate_31Wc49ZcT7cWtWGo2qbM0f_spot_bundle():
    return {
        "artist": Artist(
            id="31Wc49ZcT7cWtWGo2qbM0f",
            name="Adventures",
            popularity=29,
            genres=["alternative emo", "dreamo", "indie punk", "midwest emo"],
        ),
        "albums": [
            Album(
                id="3T9wiiFJQmTgeDXMQ4rjMx",
                name="Supersonic Home",
                release_date="2015-02-13",
                release_date_precision="day",
                total_tracks=10,
                image_url="https://i.scdn.co/image/ab67616d0000b2733d33e25ea489ec2ab60cc68d",
                album_type="album",
                artists=[ArtistRef(id="31Wc49ZcT7cWtWGo2qbM0f", name="Adventures")],
            )
        ],
    }


@fixture
def advent_candidate_3EQrIC4SwWoWnvxj4FYJpd_spot_bundle():
    return {
        "artist": Artist(
            id="3EQrIC4SwWoWnvxj4FYJpd",
            name="Adventurer",
            popularity=27,
            genres=["progressive post-hardcore", "swancore"],
        ),
        "albums": [],
    }


@fixture
def advent_candidate_0rxWZhCkYsZP6SAVTJn2BD_spot_bundle():
    return {
        "artist": Artist(
            id="0rxWZhCkYsZP6SAVTJn2BD",
            name="Músicos Adventistas",
            popularity=30,
            genres=["adventista"],
        ),
        "albums": [
            Album(
                id="5E2Ec1vHaXcFInMhiMJvFA",
                name="Musica Adventista Vol 2",
                release_date="1970-01-01",
                release_date_precision="year",
                total_tracks=12,
                image_url="https://i.scdn.co/image/ab67616d0000b273460511b7dd1b8087f7e35ae3",
                album_type="album",
                artists=[
                    ArtistRef(id="0rxWZhCkYsZP6SAVTJn2BD", name="Músicos Adventistas")
                ],
            )
        ],
    }
