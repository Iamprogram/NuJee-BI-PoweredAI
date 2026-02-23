export default function SightingsPage() {
  const sightings = [
    { city: "Phoenix", date: "2026-01-05", note: "Triangular formation moving silently." },
    { city: "Reykjavik", date: "2026-01-16", note: "Orb-like light zig-zagging over harbor." },
    { city: "Santiago", date: "2026-02-02", note: "Fast object visible for ~12 seconds." }
  ];

  return (
    <section className="space-y-5">
      <h1 className="text-3xl font-bold text-slate-900">Sightings Review Queue</h1>
      <p className="text-slate-700">
        Community submissions are screened for quality and context before appearing on the public map.
      </p>
      <ul className="grid gap-3">
        {sightings.map((sighting) => (
          <li key={`${sighting.city}-${sighting.date}`} className="glow-card">
            <p className="text-sm font-medium text-sky-700">
              {sighting.date} · {sighting.city}
            </p>
            <p className="mt-1 text-slate-700">{sighting.note}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
