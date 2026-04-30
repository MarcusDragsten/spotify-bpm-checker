import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function Navbar() {
  const { isAuthenticated, profile, login, logout } = useAuth()

  return (
    <header className="flex items-center justify-between border-b border-neutral-800 px-6 py-4">
      <Link to="/" className="flex items-center gap-2 text-lg font-semibold">
        <span className="text-spotify-green">●</span>
        <span>Vibe Checker</span>
      </Link>

      <div className="flex items-center gap-3">
        {isAuthenticated ? (
          <>
            {profile?.images?.[0]?.url ? (
              <img
                src={profile.images[0].url}
                alt=""
                className="h-8 w-8 rounded-full object-cover"
              />
            ) : (
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-neutral-700 text-xs">
                {profile?.display_name?.[0] ?? '?'}
              </div>
            )}
            <span className="text-sm text-neutral-200">
              {profile?.display_name ?? 'Spotify user'}
            </span>
            <button
              onClick={logout}
              className="rounded-full border border-neutral-700 px-3 py-1 text-xs text-neutral-300 hover:bg-neutral-800"
            >
              Log out
            </button>
          </>
        ) : (
          <button
            onClick={login}
            className="rounded-full bg-spotify-green px-4 py-2 text-sm font-medium text-black hover:bg-spotify-greenHover"
          >
            Log in with Spotify
          </button>
        )}
      </div>
    </header>
  )
}
