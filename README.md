# ReckonLight (React + Vite)

ReckonLight is an immersive educational website about end-of-civilization scenarios, aftermath systems, and human resilience.
The homepage is styled as a **real-time disaster dashboard** with a tragic, reflective mood.

## Implemented architecture

- **Framework:** React + React Router.
- **Build tool:** Vite.
- **Styling:** CSS3 with Grid/Flexbox, dark high-contrast visual system.
- **Visual mood:** dark, gritty, desaturated palette with earth-tone accents and tragic/apocalyptic atmosphere.
- **Branding:** custom candle logo (`src/assets/reckonlight-logo.svg`) integrated into the header mark.
- **UX features:** responsive navigation, hover-lift cards, smooth transitions, semantic sections.
- **Homepage design concept:** dashboard-style latest alert banner, incident feed modules, and trend bars.
- **Dashboard IA:** global alert banner → live disaster feed → impact summary statistics → scenario exploration links.
- **Header structure:** simplified Dashboard/Scenarios/About nav, live connection indicator, and high-contrast toggle.
- **Content strategy modules:** audience profiles, messaging pillars, scenario clusters, and failed doomsday predictions context.
- **Long-form content:** narrative homepage introduction, scenario previews, and deep-dive chapters for nuclear/climate/pandemic/AI scenarios.
- **Accessibility:** skip link, focus-visible styles, semantic headings/landmarks.

## Site map implemented

- Home
- Scenarios
  - Nuclear Apocalypse
  - Climate Collapse
  - Pandemic Outbreak
  - AI Takeover
  - Asteroid Impact
  - Societal Breakdown
- Aftermath
- Survival & Resilience
- Community
- Resources
- About

## Run locally

```bash
npm install
python3 backend/server.py
npm run dev
```

Start the backend first, then run Vite. Open the printed local URL (typically `http://localhost:8080`).
The frontend fetches GDACS feed data from `/api/gdacs` (proxied to `http://127.0.0.1:8000`) and refreshes every 6 minutes.

## Build

```bash
npm run build
npm run preview
```

## Render deployment (Static Site + Web Service)

This repo includes `render.yaml` for two services:

1. `reckonlight-api` (Python web service)
2. `reckonlight-frontend` (Static Site)

### Steps

1. Push this repo to GitHub.
2. In Render, choose **New +** → **Blueprint** and connect the repo.
3. Render will create both services from `render.yaml`.
4. After API is created, confirm its public URL (example: `https://reckonlight-api.onrender.com`).
5. In the frontend service environment, set:
   - `VITE_API_BASE_URL=https://<your-api-service>.onrender.com`
6. Trigger a redeploy of the frontend service.

The frontend now calls `${VITE_API_BASE_URL}/api/gdacs` in production and `/api/gdacs` in local dev.
