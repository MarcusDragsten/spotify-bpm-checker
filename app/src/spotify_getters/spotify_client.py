"""Lightweight shared Spotify API client (client-credentials flow)."""

from src.get_access_token import get_access_token


class SpotifyClient:
    """Holds a single access token + auth headers shared between getters."""

    def __init__(self) -> None:
        self.access_token = get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
