from src.spotify_getters.spotify_playlist import SpotifyPlaylist
from src.spotify_getters.spotify_track import SpotifyTrack
from src.utils.track_workout_score import calculate_workout_song_score


def get_bpm_playlist(playlist_id: str):
    playlist = SpotifyPlaylist()
    track = SpotifyTrack()

    tracks = playlist.get_playlist_tracks(playlist_id)
    tracks_with_audio_features = track.add_audio_features(tracks)

    for track_meta in tracks_with_audio_features:
        track_meta["workout_score"] = (
            calculate_workout_song_score(track_meta["audio_features"])
            if track_meta["audio_features"]
            else None
        )

    # Sort tracks by workout_score in descending order
    sorted_tracks = sorted(
        tracks_with_audio_features,
        key=lambda x: (
            x["workout_score"] if x["workout_score"] is not None else -float("inf")
        ),
        reverse=True,
    )

    return sorted_tracks
