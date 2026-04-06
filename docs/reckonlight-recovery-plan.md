# ReckonLight Architecture and Wireframe Implementation Notes

This document tracks how the repository now aligns to the requested architecture and wireframe.
It now also includes a dashboard-homepage visual adaptation with a somber disaster-monitor aesthetic.

## 1) Site Map (Implemented)

- Homepage (`/`)
- Scenarios (`/scenarios`)
  - Nuclear Apocalypse (`/scenarios/nuclear-apocalypse`)
  - Climate Collapse (`/scenarios/climate-collapse`)
  - Pandemic Outbreak (`/scenarios/pandemic-outbreak`)
  - AI Takeover (`/scenarios/ai-takeover`)
  - Asteroid Impact (`/scenarios/asteroid-impact`)
  - Societal Breakdown (`/scenarios/societal-breakdown`)
- Aftermath (`/aftermath`)
- Survival & Resilience (`/survival-resilience`)
- Community (`/community`)
- Resources (`/resources`)
- About (`/about`)

## 2) Technical Architecture (Implemented)

- Frontend Framework: React (ES6+) with React Router.
- Styling: CSS3 with CSS Grid + Flexbox responsive layout.
- Visual language: charcoal-first palette with desaturated earth/steel accents and distressed atmospheric overlays.
- Build Tool: Vite.
- Animation/Interaction: hover lift transitions, smooth visual state changes.
- Deployment fit: static hosting/CDN ready (`npm run build` outputs static assets).
- Backend feed proxy: `backend/server.py` fetches and parses GDACS RSS (`/xml/rss_24h.xml`) and serves `/api/gdacs` JSON with a 6-minute cache.

## 3) UX Flow Coverage

1. Dashboard landing with live status, alert hierarchy, and data-first module layout.
2. Priority alert review with location, timestamp, affected population, and GDACS action link.
3. Incident feed scan (last 24h) with expandable details and responsive 2/3/4-column grid, then global impact summary and trend indicators.
4. Scenario exploration via cards, risk clusters, and dedicated scenario routes.
5. Context-building through audience/messaging modules and a failed-predictions page.
6. Community and resource discovery pages for ongoing engagement.
7. Long-form narrative content on homepage, scenario deep-dives, and mission/approach framing in About.
8. Live data synchronization every 6 minutes with cached backend feed and frontend loading/error states.
9. Production deployment bootstrap includes `render.yaml` for Render Static Site + Web Service architecture.

## 4) Wireframe Mapping

### Homepage

- Navigation bar
- Hero section with title and CTA
- Introduction text
- Featured scenarios (3-column responsive grid)
- Footer

### Scenario page

- Header/title
- Overview
- Scientific Basis
- Potential Impact
- Timeline
- Related Media
- Back-navigation to Scenarios index

### Aftermath page

- Header + content cards
- Timeline block for progressive impact framing

## 5) Accessibility Coverage

- Skip-to-content link.
- High contrast dark palette.
- Focus-visible outlines for keyboard navigation.
- Semantic `<header>`, `<main>`, `<nav>`, and heading hierarchy.

## 6) Remaining enhancements (optional next step)

- Add real forum backend for Community.
- Add lightbox media galleries and true parallax for hero sections.
- Add structured SEO metadata per route.
- Add performance optimizations (image lazy loading and route-level code splitting).
- Add real animated atmospheric layer (cloud/ash shader or canvas effect) behind dashboard cards.
