import { useEffect, useRef, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { exchangeCodeForToken } from './pkce'
import { useAuth } from './AuthContext'

export default function Callback() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const { setSession } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const ranRef = useRef(false)

  useEffect(() => {
    if (ranRef.current) return
    ranRef.current = true

    const code = params.get('code')
    const errParam = params.get('error')
    if (errParam) {
      setError(errParam)
      return
    }
    if (!code) {
      setError('No authorization code returned by Spotify.')
      return
    }
    exchangeCodeForToken(code)
      .then((tokens) => {
        setSession({
          access_token: tokens.access_token,
          refresh_token: tokens.refresh_token,
          expires_in: tokens.expires_in,
        })
        navigate('/', { replace: true })
      })
      .catch((e) => setError(String(e)))
  }, [params, setSession, navigate])

  return (
    <div className="flex min-h-screen items-center justify-center px-6">
      {error ? (
        <div className="max-w-md rounded-lg border border-red-700 bg-red-900/30 p-6 text-center">
          <h2 className="mb-2 text-xl font-semibold">Login failed</h2>
          <p className="text-sm text-red-200">{error}</p>
          <button
            onClick={() => navigate('/', { replace: true })}
            className="mt-4 rounded-full bg-spotify-green px-5 py-2 text-sm font-medium text-black hover:bg-spotify-greenHover"
          >
            Back to home
          </button>
        </div>
      ) : (
        <p className="text-neutral-400">Completing Spotify login…</p>
      )}
    </div>
  )
}
