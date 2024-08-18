from typing_extensions import TypedDict


class TrackAudioFeatures(TypedDict):
    tempo: float | None
    tempo_confidence: float | None
    energy: float | None
    

class TrackMetadata(TypedDict):
    id: str
    name: str
    artists: list[str]
    album: str
    album_release_date: str
    audio_features: TrackAudioFeatures | None
