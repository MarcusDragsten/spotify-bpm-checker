import requests

from src.entities.track import TrackMetadata
from src.spotify_getters.spotify_client import SpotifyClient
from tqdm import tqdm


class SpotifyPlaylist:
    def __init__(self, client: SpotifyClient | None = None) -> None:
        self._client = client or SpotifyClient()
        self.headers = self._client.headers

    def get_playlist(self, playlist_id: str):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        resp = requests.get(url, headers=self.headers)
        playlist_json = resp.json()
        return playlist_json

    def get_next_page(self, next_page_url: str):
        print("Getting next page")
        resp = requests.get(next_page_url, headers=self.headers)
        return resp.json()

    def get_playlist_tracks(self, playlist_id: str) -> list[TrackMetadata]:
        playlist_json = self.get_playlist(playlist_id)

        if "error" in playlist_json:
            status = playlist_json["error"].get("status", 0)
            msg = playlist_json["error"].get("message", "Unknown error")
            raise ValueError(f"Spotify API error {status}: {msg}")

        tracks_obj = playlist_json["tracks"]
        tracks_list: list[TrackMetadata] = []

        while True:
            for item in tqdm(tracks_obj["items"], desc="Going through page of tracks"):
                track = item["track"]
                artists = [artist["name"] for artist in track["artists"]]
                track_data: TrackMetadata = {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": artists,
                    "album": track["album"]["name"],
                    "album_release_date": track["album"]["release_date"],
                    "preview_url": track["preview_url"],
                    #"big_image_url": track["album"]["images"][0]["url"],
                    "audio_features": None,
                    "preset_scores": None,
                }
                tracks_list.append(track_data)

            if not tracks_obj["next"]:
                break

            tracks_obj = self.get_next_page(tracks_obj["next"])

        return tracks_list
