import requests

from src.get_access_token import get_access_token
from src.entitites.track import TrackMetadata, TrackAudioFeatures
from tqdm import tqdm


class SpotifyTrack:
    def __init__(self) -> None:
        self.access_token = get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

    def chunk_list(self, lst, chunk_size):
        """Yield successive chunks from lst."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i : i + chunk_size]

    def add_audio_features(
        self, playlist_tracks: list[TrackMetadata]
    ) -> list[TrackMetadata]:
        tracks_with_audio_features: list[TrackMetadata] = []

        for chunk in tqdm(
            self.chunk_list(playlist_tracks, 100), desc="Processing tracks in chunks"
        ):
            url = f"https://api.spotify.com/v1/audio-features?ids={','.join([track['id'] for track in chunk])}"
            resp = requests.get(url, headers=self.headers)
            audio_features = resp.json()

            for track in chunk:
                for audio_feature in audio_features["audio_features"]:
                    if track["id"] == audio_feature["id"]:
                        track["audio_features"] = TrackAudioFeatures(
                            acousticness=audio_feature["acousticness"],
                            danceability=audio_feature["danceability"],
                            energy=audio_feature["energy"],
                            instrumentalness=audio_feature["instrumentalness"],
                            liveness=audio_feature["liveness"],
                            loudness=audio_feature["loudness"],
                            speechiness=audio_feature["speechiness"],
                            tempo=audio_feature["tempo"],
                            valence=audio_feature["valence"],
                        )
                        tracks_with_audio_features.append(track)
                        break

        return tracks_with_audio_features
