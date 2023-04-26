
var result = db.progSpotAlbums.aggregate([

    // Join with albums table    
    {
        $lookup:{
            from: "albums",
            localField: "spotify_id",
            foreignField: "id",
            as: "albums"
        }
    },
    {   $unwind:"$albums" },     // $unwind used for getting data in object or for one record only

    // Join with tracks table
    {
        $lookup:{
            from: "tracks",
            localField: "albums.id",
            foreignField: "_album_id",
            as: "tracks"
        }
    },
    {   $unwind:"$tracks" },     // $unwind used for getting data in object or for one record only

    // Join with audioFeatures table
    {
        $lookup:{
            from: "audioFeatures", 
            localField: "tracks.id", 
            foreignField: "id",
            as: "audioFeatures"
        }
    },
    {   $unwind:"$audioFeatures" },

    // define which fields are you want to fetch
    {   
        $project:{
            _id: 0,
            progarchives_id: 1,
            spotify_id: 1,
            
            // album
            artist: "$album.artists.name",
            album: "$albums.name",
            release_date: "$albums.release_date",
            
            // track
            track: "$tracks.name",
            disc: "$tracks.track_disc",
            number: "$tracks.track_number",
            
            // audio features
            time_signature: "$audioFeatures.time_signature",
            loudness: "$audioFeatures.loudness",
            tempo: "$audioFeatures.tempo",
            valence: "$audioFeatures.valence",
            speechiness: "$audioFeatures.speechiness",
            duration_ms: "$audioFeatures.duration_ms",
            instrumentalness: "$audioFeatures.instrumentalness",
            liveness: "$audioFeatures.liveness",
            acousticness: "$audioFeatures.acousticness",
            danceability: "$audioFeatures.danceability",
            energy: "$audioFeatures.energy",
            key: "$audioFeatures.key",
            mode: "$audioFeatures.mode"
        } 
    }
]);

db.compilation.insert(result.toArray());