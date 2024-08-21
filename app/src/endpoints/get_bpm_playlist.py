from src.spotify_getters.spotify_playlist import SpotifyPlaylist
from src.spotify_getters.spotify_track import SpotifyTrack
from src.utils.track_workout_score import calculate_workout_track_score
from src.utils.track_sleepy_score import calculate_sleepy_track_score
from src.entitites.track import PresetScores


def get_bpm_playlist(playlist_id: str):
    playlist = SpotifyPlaylist()
    track = SpotifyTrack()

    tracks = playlist.get_playlist_tracks(playlist_id)
    tracks_with_audio_features = track.add_audio_features(tracks)

    for track_meta in tracks_with_audio_features:
        if not track_meta["preset_scores"]:
            track_meta["preset_scores"] = PresetScores(
                workout=(
                    calculate_workout_track_score(track_meta["audio_features"])
                    if track_meta["audio_features"]
                    else None
                ),
                sleepy=(
                    calculate_sleepy_track_score(track_meta["audio_features"])
                    if track_meta["audio_features"]
                    else None
                ),
            )
        else:
            track_meta["preset_scores"]["workout"] = (
                calculate_workout_track_score(track_meta["audio_features"])
                if track_meta["audio_features"]
                else None
            )
            track_meta["preset_scores"]["sleepy"] = (
                calculate_sleepy_track_score(track_meta["audio_features"])
                if track_meta["audio_features"]
                else None
            )

    # Sort tracks by workout_score in descending order
    sorted_tracks = sorted(
        tracks_with_audio_features,
        key=lambda x: (
            x["preset_scores"]["workout"]
            if x["preset_scores"] and x["preset_scores"]["workout"]
            else -float("inf")
        ),
        reverse=True,
    )

    print(sorted_tracks[:5]) # Print the top 5 tracks
    top_5_tracks = sorted_tracks[:5]

    return top_5_tracks

