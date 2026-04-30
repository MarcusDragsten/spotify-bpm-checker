import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import clsx from 'clsx'
import { useAuth } from '../auth/AuthContext'
import { parsePlaylistId } from '../utils/parsePlaylistId'

export default function PlaylistInput() {
  const { isAuthenticated } = useAuth()
  const [value, setValue] = useState('')
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    if (!isAuthenticated) {
      setError('Log in with Spotify first.')
      return
    }
    const id = parsePlaylistId(value)
    if (!id) {
      setError("That doesn't look like a Spotify playlist link or ID.")
      return
    }
    navigate(`/playlist/${id}`)
  }

  return (
    <form onSubmit={handleSubmit} className="mx-auto w-full max-w-2xl px-6 pb-20">
      <label htmlFor="playlist" className="mb-2 block text-sm font-medium text-neutral-300">
        Spotify playlist link
      </label>
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          id="playlist"
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="https://open.spotify.com/playlist/…"
          className="flex-1 rounded-full border border-neutral-700 bg-neutral-900 px-5 py-3 text-sm placeholder-neutral-500 outline-none focus:border-spotify-green"
        />
        <button
          type="submit"
          disabled={!isAuthenticated}
          title={isAuthenticated ? undefined : 'Log in with Spotify to analyse playlists'}
          className={clsx(
            'rounded-full px-6 py-3 text-sm font-semibold transition',
            isAuthenticated
              ? 'bg-spotify-green text-black hover:bg-spotify-greenHover'
              : 'cursor-not-allowed bg-neutral-800 text-neutral-500',
          )}
        >
          Analyse
        </button>
      </div>
      {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
      <p className="mt-3 text-xs text-neutral-500">
        Accepts full URLs, <code>spotify:playlist:…</code> URIs, or raw playlist IDs.
      </p>
    </form>
  )
}
