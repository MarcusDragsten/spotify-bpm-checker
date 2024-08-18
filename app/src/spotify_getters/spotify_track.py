import requests

from src.get_access_token import get_access_token
from src.entitites.track import TrackMetadata, TrackAudioFeatures


class SpotifyTrack:
    def __init__(self) -> None:
        self.access_token = get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

    def add_audio_features(self, playlist_track: TrackMetadata) -> TrackMetadata:
        url = f"https://api.spotify.com/v1/audio-features/{playlist_track['id']}"
        resp = requests.get(url, headers=self.headers)
        audio_features = resp.json()

        if not playlist_track["audio_features"]:
            playlist_track["audio_features"] = TrackAudioFeatures(
                tempo=None, tempo_confidence=None, energy=audio_features["energy"]
            )
        else:
            playlist_track["audio_features"]["energy"] = audio_features["energy"]

        return playlist_track

    def add_audio_analysis(self, playlist_track: TrackMetadata) -> TrackMetadata:
        url = f"https://api.spotify.com/v1/audio-analysis/{playlist_track['id']}"
        resp = requests.get(url, headers=self.headers)
        audio_analysis = resp.json()

        if not playlist_track["audio_features"]:
            playlist_track["audio_features"] = TrackAudioFeatures(
                tempo=audio_analysis["track"]["tempo"],
                tempo_confidence=audio_analysis["track"]["tempo_confidence"],
                energy=None,
            )
        else:
            playlist_track["audio_features"]["tempo"] = audio_analysis["track"]["tempo"]
            playlist_track["audio_features"]["tempo_confidence"] = audio_analysis[
                "track"
            ]["tempo_confidence"]

        return playlist_track
