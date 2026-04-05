# ReckonLight Recovery Plan

## 1) What we could confirm from the live site

- The deployed page title is: **"When the Last Light Fades - Exploring Humanity's Final Chapter"**.
- The public URL responds through Manus hosting, but direct shell-level retrieval from this environment was blocked with HTTP 403.
- Because source and full HTML were unavailable, this repository uses a reconstruction strategy with explicit assumptions.

## 2) Inferred architecture (confidence-graded)

### High confidence

1. **Single-page narrative layout**
   - The title strongly implies a long-form storytelling landing page with sequential sections.
2. **Emphasis on visual atmosphere**
   - The language and hosting style suggest a cinematic hero section and immersive presentation.
3. **Client-side interactions**
   - Manus-generated pages commonly include lightweight front-end interaction patterns (scroll reveal, nav anchors, transitions).

### Medium confidence

1. **Mostly static content plus enhancement JS**
   - Many similar hosted microsites are static HTML/CSS with small JS enhancements.
2. **No heavy backend requirement**
   - Nothing in the available metadata implies authenticated flows or data APIs.

### Low confidence / unknowns

1. Original image/video assets.
2. Exact wording and full section structure.
3. Whether the lost source used a framework (React/Vue/Svelte) or vanilla static files.

## 3) Rebuild strategy implemented here

This recovery baseline recreates a plausible, editable version of the site architecture:

- `index.html`: hero + four story chapters + finale.
- `styles.css`: atmospheric dark theme, card sections, responsive nav.
- `app.js`: scroll progress bar + reveal animation observer.

This gives you a working scaffold now, while remaining easy to overwrite with recovered originals.

## 4) Migration path if old source is recovered

1. **Content first**: replace headings/body copy section by section.
2. **Asset restore**: reintroduce original media and typography.
3. **Interaction parity**: port original animation behavior.
4. **Tech alignment**: if original was framework-based, either:
   - keep this as static fallback, or
   - port these sections into the recovered framework component tree.
5. **URL parity checks**: ensure canonical metadata and social preview fields match production intent.

## 5) Evidence capture notes

To improve fidelity, the next helpful artifacts are:

- Any screenshot(s) of the original page (desktop/mobile).
- Saved browser source (`view-source:`) from another machine/network.
- Any previously exported Manus project JSON / prompt history.
- CDN asset URLs (images, fonts, videos) from browser DevTools network logs.
