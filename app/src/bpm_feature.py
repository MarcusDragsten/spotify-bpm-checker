from src.spotify_getters.spotify_playlist import SpotifyPlaylist
from src.spotify_getters.spotify_track import SpotifyTrack
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def get_bpm_playlist(playlist_id: str):
    playlist = SpotifyPlaylist()
    track = SpotifyTrack()

    tracks = playlist.get_playlist_tracks(playlist_id)

    for track_meta in tracks:
        track_meta = track.add_audio_features(track_meta)
        track_meta = track.add_audio_analysis(track_meta)

    return tracks


if __name__ == "__main__":
    get_bpm_playlist("4nwsUSRJvO8bRegd76PwBO")

    # https://open.spotify.com/playlist/4nwsUSRJvO8bRegd76PwBO?si=21ce5e514a59420d
