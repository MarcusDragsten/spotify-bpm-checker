import axios from 'axios'

export const apiClient = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export interface AudioFeatures {
  acousticness: number | null
  danceability: number | null
  energy: number | null
  instrumentalness: number | null
  liveness: number | null
  loudness: number | null
  speechiness: number | null
  tempo: number | null
  valence: number | null
}

export interface PresetScores {
  workout: number | null
  sleepy: number | null
}

export interface TrackResult {
  id: string
  name: string
  artists: string[]
  album: string
  album_release_date: string | null
  preview_url: string | null
  audio_features: AudioFeatures | null
  preset_scores: PresetScores | null
}

export async function fetchPlaylistAnalysis(playlistId: string): Promise<TrackResult[]> {
  const { data } = await apiClient.get<TrackResult[]>(`/playlists/${playlistId}/analysis`)
  return data
}
