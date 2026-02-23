import { featuredMysteries } from "@/lib/mock-data";

export default function WikiPage() {
  return (
    <section className="space-y-5">
      <h1 className="text-3xl font-bold text-slate-900">Mystery Wiki</h1>
      <p className="text-slate-700">
        Community-maintained case cards that prioritize source quality, context, and open questions.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        {featuredMysteries.map((mystery) => (
          <article key={mystery.title} className="glow-card">
            <h2 className="text-xl font-semibold text-sky-800">{mystery.title}</h2>
            <p className="mt-2 text-slate-700">{mystery.excerpt}</p>
            <p className="mt-3 text-xs text-slate-500">Status: Stub · Last reviewed by Agent Level-2</p>
          </article>
        ))}
      </div>
    </section>
  );
}
