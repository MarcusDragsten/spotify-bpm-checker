import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { redirectToSpotifyLogin, refreshAccessToken } from './pkce'

export interface SpotifyProfile {
  id: string
  display_name: string | null
  email?: string
  images?: { url: string }[]
}

interface StoredTokens {
  access_token: string
  refresh_token?: string
  expires_at: number // ms epoch
}

interface AuthContextValue {
  accessToken: string | null
  profile: SpotifyProfile | null
  isAuthenticated: boolean
  isLoading: boolean
  login: () => void
  logout: () => void
  setSession: (tokens: { access_token: string; refresh_token?: string; expires_in: number }) => void
}

const STORAGE_KEY = 'spotify_session'

const AuthContext = createContext<AuthContextValue | null>(null)

function loadStored(): StoredTokens | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as StoredTokens) : null
  } catch {
    return null
  }
}

async function fetchProfile(token: string): Promise<SpotifyProfile> {
  const resp = await fetch('https://api.spotify.com/v1/me', {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!resp.ok) throw new Error(`Profile fetch failed: ${resp.status}`)
  return resp.json()
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [profile, setProfile] = useState<SpotifyProfile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const refreshTimer = useRef<number | null>(null)

  const logout = useCallback(() => {
    if (refreshTimer.current) window.clearTimeout(refreshTimer.current)
    refreshTimer.current = null
    localStorage.removeItem(STORAGE_KEY)
    setAccessToken(null)
    setProfile(null)
  }, [])

  const scheduleRefresh = useCallback(
    (tokens: StoredTokens) => {
      if (refreshTimer.current) window.clearTimeout(refreshTimer.current)
      if (!tokens.refresh_token) return
      const msUntilRefresh = Math.max(tokens.expires_at - Date.now() - 60_000, 5_000)
      refreshTimer.current = window.setTimeout(async () => {
        try {
          const refreshed = await refreshAccessToken(tokens.refresh_token!)
          const next: StoredTokens = {
            access_token: refreshed.access_token,
            refresh_token: refreshed.refresh_token ?? tokens.refresh_token,
            expires_at: Date.now() + refreshed.expires_in * 1000,
          }
          localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
          setAccessToken(next.access_token)
          scheduleRefresh(next)
        } catch (err) {
          console.error('Silent refresh failed', err)
          logout()
        }
      }, msUntilRefresh)
    },
    [logout],
  )

  const setSession = useCallback(
    (tokens: { access_token: string; refresh_token?: string; expires_in: number }) => {
      const stored: StoredTokens = {
        access_token: tokens.access_token,
        refresh_token: tokens.refresh_token,
        expires_at: Date.now() + tokens.expires_in * 1000,
      }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(stored))
      setAccessToken(stored.access_token)
      scheduleRefresh(stored)
      fetchProfile(stored.access_token).then(setProfile).catch((e) => console.error(e))
    },
    [scheduleRefresh],
  )

  // Hydrate on mount
  useEffect(() => {
    const stored = loadStored()
    if (!stored) {
      setIsLoading(false)
      return
    }
    if (stored.expires_at <= Date.now() + 5_000) {
      // Expired — try refresh once
      if (stored.refresh_token) {
        refreshAccessToken(stored.refresh_token)
          .then((r) => {
            setSession({
              access_token: r.access_token,
              refresh_token: r.refresh_token ?? stored.refresh_token,
              expires_in: r.expires_in,
            })
          })
          .catch(() => {
            localStorage.removeItem(STORAGE_KEY)
          })
          .finally(() => setIsLoading(false))
        return
      }
      localStorage.removeItem(STORAGE_KEY)
      setIsLoading(false)
      return
    }
    setAccessToken(stored.access_token)
    scheduleRefresh(stored)
    fetchProfile(stored.access_token)
      .then(setProfile)
      .catch((e) => {
        console.error(e)
        logout()
      })
      .finally(() => setIsLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      accessToken,
      profile,
      isAuthenticated: !!accessToken,
      isLoading,
      login: () => void redirectToSpotifyLogin(),
      logout,
      setSession,
    }),
    [accessToken, profile, isLoading, logout, setSession],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
