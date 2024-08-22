from typing_extensions import TypedDict


class PresetScores(TypedDict):
    workout: float | None
    sleepy: float | None


class TrackAudioFeatures(TypedDict):
    acousticness: float | None
    danceability: float | None
    energy: float | None
    instrumentalness: float | None
    liveness: float | None
    loudness: float | None
    speechiness: float | None
    tempo: float | None
    valence: float | None


class TrackMetadata(TypedDict):
    id: str
    name: str
    artists: list[str]
    album: str
    album_release_date: str
    preview_url: str
    # big_image_url: str
    audio_features: TrackAudioFeatures | None
    preset_scores: PresetScores | None
