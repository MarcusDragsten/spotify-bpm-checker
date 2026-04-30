import os

import truststore; truststore.inject_into_ssl()  # use macOS Keychain for SSL verification

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.endpoints.analyze_playlist import analyze_playlist
from src.entities.track import PresetScores, TrackAudioFeatures

app = FastAPI(title="Spotify Playlist Analyzer")

# Allow the Vite dev server (and anything in CORS_ORIGINS env) to call us
_default_origins = "http://localhost:5173,http://127.0.0.1:5173"
_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", _default_origins).split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrackResult(BaseModel):
    id: str
    name: str
    artists: list[str]
    album: str
    album_release_date: str | None = None
    preview_url: str | None = None
    audio_features: TrackAudioFeatures | None = None
    preset_scores: PresetScores | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/playlists/{playlist_id}/analysis", response_model=list[TrackResult])
def get_playlist_analysis(playlist_id: str) -> list[TrackResult]:
    try:
        tracks = analyze_playlist(playlist_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return [
        TrackResult(
            id=t["id"],
            name=t["name"],
            artists=t["artists"],
            album=t["album"],
            album_release_date=t.get("album_release_date"),
            preview_url=t.get("preview_url"),
            audio_features=t.get("audio_features"),
            preset_scores=t.get("preset_scores"),
        )
        for t in tracks
    ]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
