import requests

from src.entities.track import TrackMetadata, TrackAudioFeatures
from src.spotify_getters.spotify_client import SpotifyClient
from tqdm import tqdm


class SpotifyTrack:
    def __init__(self, client: SpotifyClient | None = None) -> None:
        self._client = client or SpotifyClient()
        self.headers = self._client.headers

    def chunk_list(self, lst, chunk_size):
        """Yield successive chunks from lst."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i : i + chunk_size]

    def add_audio_features(
        self, playlist_tracks: list[TrackMetadata]
    ) -> list[TrackMetadata]:
        for chunk in tqdm(
            self.chunk_list(playlist_tracks, 100), desc="Processing tracks in chunks"
        ):
            url = f"https://api.spotify.com/v1/audio-features?ids={','.join([track['id'] for track in chunk])}"
            resp = requests.get(url, headers=self.headers)

            if resp.status_code != 200:
                print(f"Warning: /audio-features returned {resp.status_code} — skipping audio features")
                break

            data = resp.json()
            features_list = data.get("audio_features")
            if not features_list:
                print("Warning: /audio-features response has no data — endpoint may be deprecated for this app")
                break

            for track in chunk:
                for audio_feature in features_list:
                    if audio_feature and track["id"] == audio_feature["id"]:
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
                        break

        return playlist_tracks
