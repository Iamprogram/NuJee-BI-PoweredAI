import { forwardLibrary, transparencyUpdates } from "@/lib/mock-data";

export default function HomePage() {
  return (
    <section className="space-y-8">
      <div className="glow-card">
        <p className="text-xs uppercase tracking-[0.25em] text-sky-700">Hope · Transparency · Unity · Scientific Progress</p>
        <h1 className="mt-3 text-4xl font-bold text-slate-900">Horizon 2026</h1>
        <p className="mt-3 max-w-3xl text-slate-700">
          We are building a Humanity Forward Platform that prepares minds for possibility through evidence,
          responsible curiosity, and global cooperation.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <article className="glow-card">
          <h2 className="section-title">Global Transparency Dashboard</h2>
          <ul className="mt-4 space-y-3 text-slate-700">
            {transparencyUpdates.map((item) => (
              <li key={item} className="border-l-2 border-sky-300 pl-3">
                {item}
              </li>
            ))}
          </ul>
        </article>

        <article className="glow-card">
          <h2 className="section-title">Core Identity</h2>
          <p className="mt-4 text-slate-700">Prepared, not fearful. United, not divided. Curious, but evidence-led.</p>
          <p className="mt-3 text-slate-700">
            The future belongs to a humanity that can collaborate across borders, disciplines, and technologies.
          </p>
        </article>
      </div>

      <section>
        <h2 className="mb-3 section-title">Humanity Forward Library</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {forwardLibrary.map((entry) => (
            <article key={entry.title} className="glow-card">
              <p className="text-xs uppercase text-sky-700">{entry.category}</p>
              <h3 className="mt-2 text-lg font-medium text-slate-900">{entry.title}</h3>
              <p className="mt-2 text-sm text-slate-700">{entry.excerpt}</p>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
