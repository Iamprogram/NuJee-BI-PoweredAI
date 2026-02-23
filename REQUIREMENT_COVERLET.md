# PROJECT CODENAME: BEYOND-THE-EDGE
**Tagline:** *Where ET · UAP · Unknown meet the curious mind.*

## Goal
Build a lightweight, mobile-first hub that feels like a modern X-Files archive—fun, mysterious, and credible enough to keep users engaged beyond first glance.

---

## 1) Core Pillars (Must Exist)
1. **Fast News Feed**
   - Auto-aggregated stream + editor picks (UAP, SETI, fringe science).
2. **Sighting Submit**
   - 3-click submission form: text, photo, location, date.
   - Auto-map pin placement for approved sightings.
3. **Mystery Wiki**
   - Crowd-sourced cards for phenomena (e.g., Black Triangles, Wow! Signal).
4. **Community Noise**
   - Upvotes, comments, and badge progression (e.g., “Agent Level-3”).
5. **Weekend Fun**
   - Polls, quizzes, meme-of-the-week.
6. **Dark Mode by Default**
   - Core to the site’s mystery-forward brand.

---

## 2) Technical Stack (Low Cost + Scalable)
- **Frontend:** Next.js + Tailwind CSS (deployed via Vercel/Netlify static-first workflow).
- **Backend:** PlanetScale MySQL + Prisma ORM.
- **Authentication:** NextAuth (Google, Discord, email magic link).
- **File Uploads:** Cloudflare R2 (S3-compatible).
- **Search:** Typesense Cloud (nano tier).
- **News Crawl:** Node-cron + RSS-parser from ~12 vetted sources every 30 minutes.
- **Maps:** Mapbox GL JS loaded only on Sightings routes for bundle efficiency.

---

## 3) Content & Data Flow
1. Ingest external news → sanitize → classify/tag → auto-publish to **Latest**.
2. Editor can promote key items to **Featured**.
3. User sightings go to moderator queue: **approve / spam / merge duplicate**.
4. Wiki starts with stubs; trusted users can publish updates.
5. User-generated content licensed under **CC BY 4.0**.

---

## 4) Design Language
- **Palette:**
  - Midnight `#0B0C10`
  - Nebula Purple `#5B2C6F`
  - Plasma Cyan `#00E5FF`
- **Typography:** Space Grotesk (headings), Inter (body), two weights only.
- **Imagery Sources:** NASA Open Gallery, Pexels, approved generative AI assets.
- **Visual Style:** Subtle HUD vibe, light grain, 1px glow accents, micro-transitions (<150ms).
- **Accessibility Target:** Lighthouse ≥95 with keyboard support, ARIA labels, and WCAG AA contrast.

---

## 5) MVP Launch Checklist
- [ ] Home timeline with infinite scroll.
- [ ] Sighting submission with photo upload and auto-compression (<300KB).
- [ ] Basic profile (avatar, bio, agent level).
- [ ] Mystery Wiki seeded with 30 starter entries.
- [ ] Unified search across news + wiki.
- [ ] Cookie banner + GDPR “Delete My Data” flow.

---

## 6) Phase-2 (Retention Features)
- Push notifications for breaking UAP content (OneSignal).
- Weekly podcast RSS auto-generated from top summaries.
- “Night-Sky” AR mode (WebXR) for ISS/Starlink overlays.
- Gamified bounty verification + optional NFT badges (Polygon).
- AI assistant “Deep-Thought” constrained to wiki corpus.

---

## 7) Monetization (Non-Intrusive)
- Brave/BAT tip jar.
- Disclosed affiliate links (telescopes, VR, sci-fi books).
- Optional member tier ($3/mo): badge, ad-free, private Discord access.
- Explicitly avoid predatory ads/pop-up patterns.

---

## 8) Security & Legal Baseline
- Cloudflare proxy + strict CSP.
- Rate limiting on sighting submissions (e.g., 5/min/IP).
- Hash stored IPs for privacy-by-default.
- Prominent disclaimer: educational/entertainment content only.
- No medical, legal, or high-risk personal advice.

---

## 9) Delivery Timeline (Solo Dev @ 10h/week)
- **Week 1:** Repo scaffolding, CI/CD, design system.
- **Week 2:** DB schema, auth, ingestion jobs.
- **Week 3:** Sighting flow + map integration.
- **Week 4:** Wiki core + search.
- **Week 5:** UX polish, Lighthouse optimization, private beta.
- **Week 6:** Public launch + community promotion.

---

## 10) Success Metrics (First 90 Days)
- 500 registered users.
- 100 approved sightings.
- Avg. session duration > 2 minutes.
- Bounce rate < 50%.
- 0 security incidents.

---

## One-Sentence Product Positioning
**“Beyond-the-Edge is a community-powered ET/UAP mystery hub that blends credible curation, playful discovery, and social storytelling in a dark, immersive experience.”**
