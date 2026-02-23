export default function ForumPage() {
  return (
    <section className="space-y-5">
      <h1 className="text-3xl font-bold text-slate-900">Global Unity Forum</h1>
      <p className="text-slate-700">A moderated space for civil, evidence-aware discussion on humanity’s shared future.</p>
      <div className="glow-card">
        <h2 className="section-title">Forum Guardrails</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
          <li>No apocalyptic predictions or panic narratives</li>
          <li>No unverified certainty claims</li>
          <li>Respectful dialogue across perspectives</li>
        </ul>
      </div>
    </section>
  );
}
