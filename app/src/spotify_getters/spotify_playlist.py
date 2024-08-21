import requests

from src.get_access_token import get_access_token
from src.entitites.track import TrackMetadata
from tqdm import tqdm


class SpotifyPlaylist:
    def __init__(self) -> None:
        self.access_token = get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

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
                    "big_image_url": track["album"]["images"][0]["url"],
                    "audio_features": None,
                    "preset_scores": None,
                }
                tracks_list.append(track_data)

            if not tracks_obj["next"]:
                break

            tracks_obj = self.get_next_page(tracks_obj["next"])

        return tracks_list
