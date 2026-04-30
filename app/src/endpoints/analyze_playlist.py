"""Analyze a Spotify playlist: fetch tracks, attach audio features, compute preset scores."""

from src.entities.track import PresetScores, TrackMetadata
from src.spotify_getters.spotify_client import SpotifyClient
from src.spotify_getters.spotify_playlist import SpotifyPlaylist
from src.spotify_getters.spotify_track import SpotifyTrack
from src.utils.track_sleepy_score import calculate_sleepy_track_score
from src.utils.track_workout_score import calculate_workout_track_score


def _safe_workout(features) -> float | None:
    if not features:
        return None
    try:
        return calculate_workout_track_score(features)
    except AssertionError:
        return None


def _safe_sleepy(features) -> float | None:
    if not features:
        return None
    try:
        return calculate_sleepy_track_score(features)
    except AssertionError:
        return None


def analyze_playlist(playlist_id: str) -> list[TrackMetadata]:
    """Return every track in the playlist with audio features + preset scores."""
    client = SpotifyClient()
    playlist = SpotifyPlaylist(client)
    track = SpotifyTrack(client)

    tracks = playlist.get_playlist_tracks(playlist_id)
    tracks_with_audio_features = track.add_audio_features(tracks)

    for track_meta in tracks_with_audio_features:
        features = track_meta["audio_features"]
        track_meta["preset_scores"] = PresetScores(
            workout=_safe_workout(features),
            sleepy=_safe_sleepy(features),
        )

    return tracks_with_audio_features
