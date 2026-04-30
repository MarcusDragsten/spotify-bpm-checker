/** Parse a Spotify playlist URL, URI, or raw ID into the bare ID. */
const PLAYLIST_ID_RE = /^[A-Za-z0-9]{22}$/

export function parsePlaylistId(input: string): string | null {
  const value = input.trim()
  if (!value) return null

  if (PLAYLIST_ID_RE.test(value)) return value

  // spotify:playlist:<id>
  const uriMatch = value.match(/^spotify:playlist:([A-Za-z0-9]{22})$/)
  if (uriMatch) return uriMatch[1]

  // https://open.spotify.com/playlist/<id>?si=...
  // Also accept regional prefixes like /intl-en/
  const urlMatch = value.match(/open\.spotify\.com\/(?:[a-zA-Z-]+\/)?playlist\/([A-Za-z0-9]{22})/)
  if (urlMatch) return urlMatch[1]

  return null
}
