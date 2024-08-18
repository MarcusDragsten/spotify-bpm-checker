import requests

from src.get_access_token import get_access_token

access_token = get_access_token()

def get_playlist(playlist_id: str):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    resp = requests.get(url, headers=headers)
    
    #json = resp.json()["tracks"]["items"][0]["track"]["artists"]
    json = len(resp.json()["tracks"]["items"])
    
    
    
    print(json)
    
    
if __name__ == "__main__":
    get_playlist("5W5rQIkSsjlsdQoyxnMNIZ")


#curl --request GET \
#  --url https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n \
#  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'

