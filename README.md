# spotify-bpm-checker

Analyze a Spotify playlist's tracks for tempo, energy, and "vibe fit" — surface the songs that don't match the rest of the playlist.

Stack:

- **Backend**: FastAPI (Python 3.12, Poetry)
- **Frontend**: React 18 + Vite + TypeScript + Tailwind CSS
- **Auth**: Spotify OAuth 2.0 with PKCE (browser-only)

## Project layout

```
app/         FastAPI backend
frontend/    React + Vite frontend
```

## Backend setup

1. From the repo root, create and activate a virtualenv:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install poetry
   ```
2. Install dependencies:
   ```bash
   cd app
   poetry install
   ```
3. Create `.env` in the repo root with your Spotify app credentials (used for the client-credentials flow that powers playlist analysis):
   ```bash
   CLIENT_ID=<your_spotify_client_id>
   CLIENT_SECRET=<your_spotify_client_secret>
   ```
4. Run the API:
   ```bash
   cd app
   PYTHONPATH=. uvicorn main:app --reload --port 8000
   ```

Endpoints:

- `GET /health` — sanity check
- `GET /playlists/{playlist_id}/analysis` — returns every track in the playlist with audio features and `workout`/`sleepy` preset scores

## Frontend setup

1. **Configure your Spotify app dashboard** — at https://developer.spotify.com/dashboard, edit your app and add this Redirect URI:
   ```
   http://127.0.0.1:5173/callback
   ```
2. Install deps and configure env:
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # edit .env.local and set VITE_SPOTIFY_CLIENT_ID
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```
4. Open http://127.0.0.1:5173. The Vite dev server proxies `/api/*` to the FastAPI backend on port 8000.

## Notes

- The frontend uses **PKCE** so the Spotify Client Secret never leaves the backend.
- Access tokens are kept in `localStorage` for dev convenience. If this ever ships publicly, move the OAuth exchange behind the backend with httpOnly cookies.
- Playlist analysis itself uses the backend's client-credentials token — the user's token is only used for the login UX and (later) listing the user's own playlists.
