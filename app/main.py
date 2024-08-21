from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Assuming the get_bpm_playlist function is imported from endpoints.py
from src.endpoints.get_bpm_playlist import get_bpm_playlist


class TrackMeta(BaseModel):
    id: str
    name: str
    preset_scores: list[dict[str, float | None]]


@app.get("/bpm-playlist/{playlist_id}", response_model=list[TrackMeta])
def get_playlist(playlist_id: str):
    playlist_tracks = get_bpm_playlist(playlist_id)
    
    
    
    track_metas: list[TrackMeta] = [
        TrackMeta(
            id=track["id"],
            name=track["name"],
            preset_scores=[],
        )
        for track in playlist_tracks
    ]


    return track_metas


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
