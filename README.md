# ReckonLight (Recovery Build)

This repository contains a **reconstructed baseline** for the lost ReckonLight site previously hosted at:

- https://cyywlknc.manus.space/

Because the original source code is unavailable, this build focuses on:

1. Recreating the likely information architecture and storytelling flow.
2. Providing a clean, editable static implementation.
3. Documenting assumptions so the original source can be merged in later.

## Quick start

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Project structure

- `index.html` — page structure and content sections.
- `styles.css` — visual system, gradients, spacing, and responsive behavior.
- `app.js` — scroll reveal, progress indicator, and smooth anchor navigation.
- `docs/reckonlight-recovery-plan.md` — architecture analysis, assumptions, and migration plan.

## Next recovery steps

- Replace placeholder content with any recovered copy blocks.
- Swap background/media assets if you locate originals.
- If old source is found, use the migration checklist in `docs/reckonlight-recovery-plan.md`.
