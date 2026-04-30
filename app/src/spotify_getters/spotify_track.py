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

    RECCOBEATS_URL = "https://api.reccobeats.com/v1/audio-features"
    RECCOBEATS_BATCH_SIZE = 40

    def add_audio_features(
        self, playlist_tracks: list[TrackMetadata]
    ) -> list[TrackMetadata]:
        for chunk in tqdm(
            self.chunk_list(playlist_tracks, self.RECCOBEATS_BATCH_SIZE),
            desc="Fetching audio features",
        ):
            ids_param = "&".join(f"ids={track['id']}" for track in chunk)
            url = f"{self.RECCOBEATS_URL}?{ids_param}"
            resp = requests.get(url, headers={"Accept": "application/json"})

            if resp.status_code != 200:
                print(f"Warning: ReccoBeats returned {resp.status_code} — skipping chunk")
                continue

            data = resp.json()
            features_list = data.get("content")
            if not features_list:
                continue

            # Build a lookup from Spotify track ID → features
            href_to_features: dict[str, dict] = {}
            for feat in features_list:
                href = feat.get("href", "")
                # href is like "https://open.spotify.com/track/<spotify_id>"
                spotify_id = href.rsplit("/", 1)[-1] if href else None
                if spotify_id:
                    href_to_features[spotify_id] = feat

            for track in chunk:
                feat = href_to_features.get(track["id"])
                if feat:
                    track["audio_features"] = TrackAudioFeatures(
                        acousticness=feat.get("acousticness"),
                        danceability=feat.get("danceability"),
                        energy=feat.get("energy"),
                        instrumentalness=feat.get("instrumentalness"),
                        liveness=feat.get("liveness"),
                        loudness=feat.get("loudness"),
                        speechiness=feat.get("speechiness"),
                        tempo=feat.get("tempo"),
                        valence=feat.get("valence"),
                    )

        return playlist_tracks
