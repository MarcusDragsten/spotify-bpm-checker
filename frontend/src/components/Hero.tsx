export default function Hero() {
  return (
    <section className="mx-auto max-w-3xl px-6 pt-20 pb-10 text-center">
      <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
        Find the songs that <span className="text-spotify-green">don't fit your vibe</span>
      </h1>
      <p className="mt-4 text-base text-neutral-400 sm:text-lg">
        Paste any Spotify playlist link and we'll analyse every track — tempo, energy, mood —
        and surface the ones that stick out from the rest.
      </p>
    </section>
  )
}
