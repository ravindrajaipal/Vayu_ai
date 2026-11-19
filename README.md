# VayuAI Pro v4.0 (Zero-API-Key Live Edition) — GenAI Urban Air Quality & Winter Smog Operating System
**PromptWars Virtual — [Challenge 6] Urban Air Quality Assistant**

## 1. Project Overview
**VayuAI Pro v4.0 (Zero-API-Key Live Edition)** is a production-ready, responsive web application and urban air quality decision engine designed for families, university hostels, and residential communities navigating severe winter smog across Indian cities. It combines real-time CPCB National Air Quality Index (NAQI) telemetry, CAQM Graded Response Action Plan (GRAP Stage I–IV) protocols, WHO 2021 Air Quality Guidelines, room-level Clean Air Delivery Rate (CADR) physics, respirator inward-leakage modeling, and ITF-OECD life-cycle transport emission math into a single interactive interface.

## 2. Problem Statement
During winter temperature inversions across the Indo-Gangetic Plain and urban India, the atmospheric boundary layer drops below 100 metres, locking fine particulate matter (`PM2.5` and `PM10`) near ground level. Families and students face three critical gaps:
1. **Misleading Linear AQI Interpretation**: Most citizens do not realize that morning inversion peaks (`06:00–09:00`) are drastically more toxic than the afternoon solar mixing window (`13:00–16:00`), or that unsealed N95/cloth masks leak `27%–58%` of ambient PM2.5.
2. **High Cost of Commercial Air Purifiers**: Commercial True HEPA purifiers (`~$549` / `₹40,000+` for `282 CFM`) are unaffordable for most households and student hostels, whereas peer-reviewed DIY MERV-13 Corsi-Rosenthal boxes achieve `600–850 CFM` (`70%–92%` PM2.5 reduction) at `~1/10th` the cost (`$0.08/CADR`).
3. **Invisible Personal Emission Impact**: Commuters and households lack clear, quantified feedback showing how daily choices (switching from private/shared cars to electric buses or cycling, running kitchen exhaust hoods, and eliminating indoor incense/biomass burning) directly lower both indoor exposure and urban emissions.

## 3. Features
- **Tab 1 — AI Smog Radar & Co-Pilot**:
  - Pre-loaded November 2026 CPCB telemetry for **Delhi NCR** (`AQI 367`, `PM2.5 218 µg/m³`), **Jodhpur** (`AQI 265`, `PM2.5 131.2 µg/m³`), **Jaipur** (`AQI 237`, `PM2.5 149.17 µg/m³`), and **Mumbai** (`AQI 146`, `PM2.5 64 µg/m³`) + custom AQI simulation slider (`35–500`).
  - **Berkeley Earth Cigarette Equivalence Meter** (`22 µg/m³` PM2.5 over 24h ≈ 1 cigarette/day) comparing unfiltered outdoor air vs. filtered indoor sanctuary.
  - **Transparent AI Co-Pilot**: Explicitly badges whether responses come from the **Deterministic CPCB/WHO Domain Engine** (offline-capable, zero-latency math) or the **Live Gemini 2.5 Flash API**, with English + Hinglish explanations and **🔊 Voice AI** (`speechSynthesis`) read-aloud.
  - **24-Hour Boundary Layer & Smog Inversion Chart** (`Chart.js`).
- **Tab 2 — Low-Emission 24-Hour Routines & Respirator Fit Lab**:
  - Interactive 6-slot daily schedule builder with real-time keyword search/filter (`#routineFilterInput`), empty-state handling, and **↺ Reset** button.
  - **Respirator Mask Fit-Leakage Simulator**: Compares N95 Airtight Seal (`97.2%`), FFP2 (`94.0%`), N95 with `27%` Inward Fit Leakage (`70.0%`), 3-Ply Surgical (`70.0%`), Cotton Cloth (`41.6%`), Muslin (`37.8%`), and Sponge (`33.5%`) masks.
- **Tab 3 — Indoor Air Quality (IAQ) Hacks, CADR Lab & 2D 4-Zone Floorplan**:
  - **Room CADR & 60-Minute Decay Simulator**: Models 5 filtration setups (`680 CFM` 5-filter MERV-13 Corsi-Rosenthal Box, `405 CFM` 5" MERV-13, `322 CFM` 4" MERV-13, `293 CFM` 2" MERV-13, and `282 CFM` Commercial HEPA) across `100–600 sq ft` rooms and window seal states.
  - **Interactive 2D Home & Hostel 4-Zone Airflow Floorplan (`Z1–Z4`)**: Clickable room zones (`Z1` Living/Study, `Z2` Kitchen & Tarka Exhaust, `Z3` Sealed Sleep Sanctuary, `Z4` Balcony & Entry Airlock) paired with the **1989 NASA Clean Air Study VOC & Humidity Matrix** (`Snake Plant`, `Areca Palm`, `Peace Lily`, `Spider Plant`).
- **Tab 4 — Sustainable Alternatives & Direct Impact Modeler**:
  - Grounded in **ITF-OECD India LCA**, **Our World in Data**, **CEEW**, and **WRI India** (`₹12,118/tCO₂e` societal abatement value), modeling shifts from private cars/shared cabs/2-wheelers to Electric Buses (`-71%` to `-79%`), Cycling (`-75%`), and Metro + EV 2-Wheelers (`-68%`).
- **Tab 5 — Community & Campus Shield**:
  - Scales impact across `10–500` households or hostel rooms, generating a **Bilingual WhatsApp Smog Advisory** and a downloadable **`.SVG` Clean-Air Protocol Poster**.
- **Tab 6 — PromptWars Export & Submission Hub**:
  - 1-click copy boxes (`<100`, `<240`, and `<1024` chars) + `.JSON` blueprint export, `.MD` report export, and printable PDF dossier (`window.print()`).

## 4. Technology Stack
- **Frontend**: Semantic HTML5, Tailwind CSS (`3.4.17` via CDN), Vanilla ES2022 JavaScript, Chart.js (`4.4.1` via jsDelivr), Web Speech API (`speechSynthesis`).
- **Backend (Optional Vercel Serverless Proxy)**: Node.js Serverless Function (`api/gemini.js`) communicating with Google Gemini 2.5 Flash (`generativelanguage.googleapis.com`).
- **Testing & QA**: Python 3 (`unittest`, `BeautifulSoup4`), Node.js (`v18+`) serverless unit/integration harness, and Headless Chromium DOM verification.

## 5. Architecture
```text
vayu_ai_repo/
├── index.html               # Self-contained, XSS-hardened SPA (works standalone & in Canvas)
├── api/
│   └── gemini.js            # Vercel Serverless Function proxy (reads process.env.GEMINI_API_KEY)
├── tests/
│   └── test_suite.py        # Automated Unit, Integration, API, Security & Accessibility test suite
├── vercel.json              # Vercel routing + HTTP security headers (CSP-compatible, nosniff, SAMEORIGIN)
├── .env.example             # Environment variable template (never commit real keys)
├── .gitignore               # Excludes .env, node_modules, .vercel
├── SUBMISSION_ANSWERS.txt   # Ready-to-paste PromptWars portal answers
└── README.md                # Full project documentation
```

## 6. Installation Instructions
```bash
# Clone the repository
git clone https://github.com/<your-username>/vayu-ai-urban-air-assistant.git
cd vayu-ai-urban-air-assistant

# Serve locally using Python or Node/Vercel CLI
python3 -m http.server 8080
# Open http://localhost:8080 in your browser
```

## 7. Environment Variable Setup
To enable the server-side Gemini API proxy on Vercel without exposing keys in browser code:
1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```
2. Add your Google Gemini API key:
   ```ini
   GEMINI_API_KEY=your_actual_gemini_api_key
   ```
3. In the Vercel Dashboard, go to **Project Settings → Environment Variables** and add `GEMINI_API_KEY`.

## 8. API Configuration
- **Zero-API-Key Live Air Quality (Default)**: Uses [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) (`geocoding-api.open-meteo.com/v1/search`) and [Open-Meteo CAMS Air Quality API](https://open-meteo.com/en/docs/air-quality-api) (`air-quality-api.open-meteo.com/v1/air-quality`) directly from the browser with **no API key or credit card required**.
- **Serverless Endpoint (`POST /api/gemini`)**: Accepts JSON `{ city, aqi, pm25, profile, prompt }` (up to 280 chars), validates types and ranges, enforces an `8,000ms` `AbortController` timeout, and returns `{ text, sourceMode }`.
- **In-Memory Session Key**: For static sandbox previews where no backend server runs, users can click **✨ AI Engine: Ready** in the top navigation bar to supply a temporary session API key held strictly in JavaScript memory (never written to `localStorage` or disk).
- **Deterministic Fallback**: When no API key is provided, the app executes its built-in **Deterministic CPCB/WHO Rule Engine** and explicitly labels every card so simulated output is never misrepresented as a live LLM call.

## 9. Testing Instructions
Run the automated verification and test suite:
```bash
python3 tests/test_suite.py
```
The test suite executes unit math checks, DOM/accessibility audits, XSS injection defenses, Node.js serverless handler tests (`405`, `400`, `503`), and Headless Chromium rendering checks.

## 10. Deployment Instructions (GitHub + Vercel)
1. Push all files in this directory to a **Public GitHub Repository**.
2. Log in to [Vercel](https://vercel.com), click **Add New Project**, and import your GitHub repository.
3. Keep **Framework Preset** as **Other** (static + `api/` serverless function auto-detected via `vercel.json`).
4. (Optional) Add `GEMINI_API_KEY` under **Environment Variables**.
5. Click **Deploy** — your live `.vercel.app` URL will be ready in ~10–15 seconds.

## 11. Assumptions and Limitations
- **Offline / Sandbox Preview Limitation**: Inside a static file preview without a backend or user-supplied session key, live LLM calls cannot run; the app transparently defaults to its **Deterministic CPCB/WHO Rule Engine** and labels all outputs accordingly.
- **Telemetry Snapshots**: The 4 city presets (`Delhi NCR`, `Jodhpur`, `Jaipur`, `Mumbai`) use verified November 2026 CPCB/MPCB station readings as baseline defaults and allow real-time user simulation from `AQI 35` to `500`.
- **Berkeley Earth & NASA Study Scope**: The `22 µg/m³ = 1 cigarette/day` metric is a population-level cardiovascular/respiratory risk communication aid (Pope et al. / Berkeley Earth), and NASA Clean Air Study houseplants are presented strictly as VOC/humidity companions alongside high-CADR HEPA/MERV-13 mechanical filtration, not replacements for particulate filters.
