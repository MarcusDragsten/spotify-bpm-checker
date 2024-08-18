import requests

from src.config_setup import config


def get_access_token() -> str:
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    body = {
        "grant_type": "client_credentials",
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
    }

    resp = requests.post(url, headers=headers, data=body)
    resp.raise_for_status()
    
    return resp.json()["access_token"]
