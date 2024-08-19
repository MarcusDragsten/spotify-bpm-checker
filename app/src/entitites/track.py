from typing_extensions import TypedDict


class TrackAudioFeatures(TypedDict):
    danceability: float | None
    tempo: float | None
    energy: float | None
    valence: float | None


class TrackMetadata(TypedDict):
    id: str
    name: str
    artists: list[str]
    album: str
    album_release_date: str
    audio_features: TrackAudioFeatures | None
    workout_score: float | None
