export default function SubmitPage() {
  return (
    <section className="max-w-2xl space-y-6">
      <h1 className="text-3xl font-bold text-slate-900">Submit a Sighting</h1>
      <p className="text-slate-700">
        Share what you observed with enough detail for moderators to evaluate responsibly.
      </p>
      <form className="glow-card grid gap-4">
        <label className="grid gap-2 text-sm text-slate-700">
          Description
          <textarea
            className="min-h-28 rounded-md border border-sky-200 bg-white px-3 py-2 text-slate-900"
            placeholder="What did you see?"
          />
        </label>
        <label className="grid gap-2 text-sm text-slate-700">
          Location
          <input
            className="rounded-md border border-sky-200 bg-white px-3 py-2 text-slate-900"
            placeholder="City, Country"
          />
        </label>
        <label className="grid gap-2 text-sm text-slate-700">
          Date
          <input type="date" className="rounded-md border border-sky-200 bg-white px-3 py-2 text-slate-900" />
        </label>
        <button type="submit" className="rounded-md bg-sky-600 px-4 py-2 font-semibold text-white hover:bg-sky-700">
          Send to Moderator Queue
        </button>
      </form>
    </section>
  );
}
