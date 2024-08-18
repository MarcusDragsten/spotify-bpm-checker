import requests

from src.get_access_token import get_access_token

from typing_extensions import TypedDict


class PlaylistTrack(TypedDict):
    id: str
    name: str
    artists: list[str]
    album: str
    album_release_date: str


class SpotifyPlaylist:
    def __init__(self) -> None:
        self.access_token = get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_playlist(self, playlist_id: str) -> dict:
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        resp = requests.get(url, headers=self.headers)
        playlist_json = resp.json()
        return playlist_json
    
    def get_next_page(self, next_page_url: str):
        resp = requests.get(next_page_url, headers=self.headers)
        return resp.json()
        

    def get_playlist_tracks(self, playlist_id: str):
        playlist_json = self.get_playlist(playlist_id)

        tracks_obj = playlist_json["tracks"]
        tracks_list: list[PlaylistTrack] = []
        
        while tracks_obj["next"]:
            next_page = self.get_next_page(tracks_obj["next"])
            for item in next_page["items"]:
                track = item["track"]
                artists = [artist["name"] for artist in track["artists"]]
                track_data: PlaylistTrack = {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": artists,
                    "album": track["album"]["name"],
                    "album_release_date": track["album"]["release_date"],
                }
                tracks_list.append(track_data)
                
            tracks_obj = next_page
            

        print(len(tracks_list))
        print(tracks_list[0])


if __name__ == "__main__":
    cl = SpotifyPlaylist()
    cl.get_playlist_tracks("5W5rQIkSsjlsdQoyxnMNIZ")
