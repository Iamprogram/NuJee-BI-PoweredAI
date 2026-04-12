# Unknown Beyond Architecture Analysis (inferred)

## What was analyzed
The live site at `https://pcxhrmwh.gensparkspace.com/` appears to be a static multipage website with:

- Shared top navigation and footer across pages.
- Primary pages: Home, Library, Map, Timeline, Community, Resources, About.
- Content-oriented layout (hero, metric badges, cards, disclaimers).
- Lightweight/no-obvious backend requirement for baseline rendering.

## Inferred implementation style

1. **Frontend stack**: Static HTML + CSS + minimal JavaScript.
2. **Routing model**: Page-per-route (`index.html`, `library.html`, etc.) rather than SPA.
3. **Design system**: Dark, cosmic visual theme with card components and status labels.
4. **Content model**:
   - Featured incidents/news blocks.
   - Category buckets with counts.
   - Credibility framework labels.
5. **Likely deployment**: Static hosting/CDN (fast global edge-delivery pattern).

## What was replicated in this repository
- A static multi-page structure mirroring the information architecture.
- Shared stylesheet (`assets/styles.css`) for reusable UI primitives.
- Shared script (`assets/app.js`) for active nav state + dynamic year.
- Placeholder sections where external systems would later plug in (e.g., map data source).

## If you recover previous source code later
Use this migration order:

1. Replace page content blocks while preserving layout classes.
2. Reconnect data sources (map markers, timeline feed, report catalogs).
3. Add form handlers/auth only after static parity is complete.
4. Validate legal pages and outbound references.

