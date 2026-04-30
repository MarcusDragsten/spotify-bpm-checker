import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchPlaylistAnalysis, type TrackResult } from '../api/client'

type SortKey = 'workout' | 'sleepy' | 'tempo' | 'energy' | 'name'

export default function PlaylistResults() {
  const { id } = useParams<{ id: string }>()
  const [tracks, setTracks] = useState<TrackResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [sortKey, setSortKey] = useState<SortKey>('workout')

  useEffect(() => {
    if (!id) return
    setLoading(true)
    setError(null)
    fetchPlaylistAnalysis(id)
      .then(setTracks)
      .catch((e) => setError(e?.message ?? 'Failed to load playlist'))
      .finally(() => setLoading(false))
  }, [id])

  const sorted = useMemo(() => {
    if (!tracks) return []
    const copy = [...tracks]
    copy.sort((a, b) => {
      const get = (t: TrackResult): number => {
        switch (sortKey) {
          case 'workout':
            return t.preset_scores?.workout ?? -Infinity
          case 'sleepy':
            return t.preset_scores?.sleepy ?? -Infinity
          case 'tempo':
            return t.audio_features?.tempo ?? -Infinity
          case 'energy':
            return t.audio_features?.energy ?? -Infinity
          case 'name':
            return 0
        }
      }
      if (sortKey === 'name') return a.name.localeCompare(b.name)
      return get(b) - get(a)
    })
    return copy
  }, [tracks, sortKey])

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <Link to="/" className="mb-6 inline-block text-sm text-neutral-400 hover:text-white">
        ← Back
      </Link>

      <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Playlist analysis</h1>
          <p className="text-sm text-neutral-500">ID: {id}</p>
        </div>
        <label className="text-sm text-neutral-400">
          Sort by{' '}
          <select
            value={sortKey}
            onChange={(e) => setSortKey(e.target.value as SortKey)}
            className="ml-2 rounded-md border border-neutral-700 bg-neutral-900 px-2 py-1 text-white"
          >
            <option value="workout">Workout score</option>
            <option value="sleepy">Sleepy score</option>
            <option value="tempo">Tempo</option>
            <option value="energy">Energy</option>
            <option value="name">Name (A–Z)</option>
          </select>
        </label>
      </div>

      {loading && <p className="text-neutral-400">Analysing playlist…</p>}
      {error && (
        <div className="rounded-lg border border-red-700 bg-red-900/30 p-4 text-sm text-red-200">
          {error}
        </div>
      )}

      {sorted.length > 0 && (
        <div className="overflow-x-auto rounded-lg border border-neutral-800">
          <table className="w-full text-left text-sm">
            <thead className="bg-neutral-900 text-xs uppercase tracking-wide text-neutral-400">
              <tr>
                <th className="px-4 py-3">Track</th>
                <th className="px-4 py-3">Artists</th>
                <th className="px-4 py-3 text-right">BPM</th>
                <th className="px-4 py-3 text-right">Energy</th>
                <th className="px-4 py-3 text-right">Workout</th>
                <th className="px-4 py-3 text-right">Sleepy</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((t) => (
                <tr key={t.id} className="border-t border-neutral-800 hover:bg-neutral-900/60">
                  <td className="px-4 py-3 font-medium">{t.name}</td>
                  <td className="px-4 py-3 text-neutral-400">{t.artists.join(', ')}</td>
                  <td className="px-4 py-3 text-right tabular-nums">
                    {fmt(t.audio_features?.tempo, 0)}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums">
                    {fmt(t.audio_features?.energy, 2)}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums text-spotify-green">
                    {fmt(t.preset_scores?.workout, 2)}
                  </td>
                  <td className="px-4 py-3 text-right tabular-nums text-indigo-300">
                    {fmt(t.preset_scores?.sleepy, 2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {!loading && tracks && tracks.length === 0 && (
        <p className="text-neutral-400">No tracks found in this playlist.</p>
      )}
    </div>
  )
}

function fmt(n: number | null | undefined, digits: number): string {
  if (n === null || n === undefined) return '—'
  return n.toFixed(digits)
}
