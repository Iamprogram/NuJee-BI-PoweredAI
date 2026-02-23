export default function DashboardPage() {
  return (
    <section className="space-y-5">
      <h1 className="text-3xl font-bold text-slate-900">Global Transparency Dashboard</h1>
      <p className="text-slate-700">
        Tracking humanity’s expanding knowledge across space missions, scientific publications, responsible
        disclosures, and AI breakthroughs.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        <article className="glow-card">
          <h2 className="section-title">Current Focus</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
            <li>Space mission milestones</li>
            <li>Government declassification updates</li>
            <li>Publicly verifiable research releases</li>
          </ul>
        </article>
        <article className="glow-card">
          <h2 className="section-title">Principle</h2>
          <p className="mt-3 text-slate-700">
            We frame change as progress in shared understanding—not as fear-based exposure narratives.
          </p>
        </article>
      </div>
    </section>
  );
}
