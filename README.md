# AquaPulse — Freshwater Event Intelligence

> **See the signal. Remember the pattern. Anticipate the next event.**

AquaPulse is an explainable freshwater event-intelligence prototype for urban river resilience. The first study area is **Dehradun, Uttarakhand**, using the Bindal/Rispana context.

The product loop is:

`Observe → Detect → Correlate → Remember → Predict → Prioritize → Verify → Learn`

## What AquaPulse demonstrates

AquaPulse combines environmental signals, rainfall context, citizen observations, spatial/temporal coherence and an event-memory library to produce an **environmental event hypothesis** and prioritize locations for human verification.

It deliberately does **not** claim that a single measurement proves pollution, toxicity, health risk, antibiotic-resistance genes, or another laboratory-only property.

### Core product surfaces

- **Command Center** — event confidence, evidence mix, fingerprint, map and intelligence loop.
- **River Memory™** — compares the current signature with prior event patterns.
- **Hot Moments** — identifies a vulnerability window for prioritization.
- **Verification Centre** — ranks field-investigation locations while keeping the final call with a human.
- **Evidence & Provenance** — distinguishes REAL, DERIVED and SIMULATED information.
- **AquaPulse Guide** — an evidence-aware in-product chatbot that explains the current event, evidence, River Memory, Hot Moments, provenance and verification priorities without inventing live data.
- **Guided Demo Mode** — cycles through the three prepared event stories for a clean presentation.

## Final project status

This ZIP is the **single final project package** after the final feature pass. It includes the seven planned submission refinements: One Health impact framing, an explainable reasoning panel, clearer prototype-vs-production data boundaries, an honest Gurugram preview, hardened demo mode, final navigation/UX hardening, and the AquaPulse Guide chatbot.

This ZIP is the **single final project package**. It supersedes the earlier v0.x build archives. Keep this extracted folder as the working copy for local testing and subsequent fixes.

The high-frequency event scenarios are intentionally **SIMULATED DEMO DATA**. Official CPCB records and research sources are used as contextual evidence; they are not presented as live current-event telemetry.

## Architecture

```text
React + Vite + Leaflet
          │
          ▼
      FastAPI API
          │
   ┌──────┼──────────┐
   ▼      ▼          ▼
Data   Intelligence  State
   │      │          │
   │      ├─ Fusion
   │      ├─ Fingerprint
   │      ├─ River Memory
   │      ├─ Hot Moments
   │      ├─ Propagation
   │      └─ Verification
   │
   ├─ CPCB contextual records
   ├─ NASA GPM IMERG adapter
   ├─ Sentinel-2 contextual registry
   └─ simulated demo signals
```

## Data provenance

Every source is treated as one of:

- **REAL** — copied/normalized from an official public or research source.
- **DERIVED** — calculated by AquaPulse from available observations or study-area geometry.
- **SIMULATED** — generated for the controlled demo because a continuous observation stream is not available in this package.

### Real/contextual evidence

- CPCB Dehradun Rispana/Bindal drain observations: `backend/data/real/cpcb_dehradun_drain_samples.csv`
- CPCB publications: https://cpcb.nic.in/publications-3/
- NASA GPM IMERG: https://gpm.nasa.gov/data/imerg
- Copernicus Sentinel-2 water-body context: https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Water_bodies
- 2026 Scientific Reports Dehradun river study: https://www.nature.com/articles/s41598-026-66240-7
- 2026 Environmental Pollution study on monsoon-triggered ARG surges in urban Indian rivers: https://pubmed.ncbi.nlm.nih.gov/42218970/

## Windows 11 setup — recommended path

Use **one** Python environment at the project root. Do not create a second `.venv` inside `backend/`. PowerShell activation is optional and not required.

### 1. Backend

Open **PowerShell** in the project root (the folder containing `README.md` and `backend/`):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then run the smoke test:

```powershell
.\.venv\Scripts\python.exe tests_smoke.py
```

Backend health: http://127.0.0.1:8000/health  
API docs: http://127.0.0.1:8000/docs

### 2. Start backend

**Recommended on Windows:**

```powershell
.\run_backend.cmd
```

The Windows `.cmd` launcher uses the root `.venv` directly and avoids PowerShell execution-policy / downloaded-file signing restrictions. The `.ps1` launcher is also included for environments where script execution is permitted.

### 3. Frontend

Open a **second terminal** and use:

```powershell
.\run_frontend.cmd
```

Or manually:

```powershell
cd frontend
npm install
npm run dev
```

Open: http://127.0.0.1:5173

Node.js 20.19+ is required; Node 22.12+ (including Node 22 LTS) is suitable.

### If PowerShell blocks `.ps1` files
Use the `.cmd` launchers or the manual commands above. Downloaded ZIPs can carry a Windows file-origin mark that causes PowerShell to block unsigned `.ps1` files. Do not change the system execution policy globally just to run AquaPulse.

## Final UI behavior

- Top navigation is interactive and updates the active section, URL hash and scroll position.
- Starting Demo Mode pauses automatically when a different section is opened so the selected page does not unexpectedly change.
- The study-area selector currently enables only the validated Dehradun prototype dataset; additional cities are intentionally disabled until validated local data is connected.
- The Leaflet map revalidates its dimensions after rendering and resizing to avoid blank tile regions when the layout changes.
- Scenario refreshes keep the current page rendered while the new event intelligence loads, reducing tab/refresh white screens.
- Citizen-report and verification failures are surfaced to the user instead of failing silently.
- The study-area dropdown supports Dehradun and a clearly labelled Gurugram preview, with no fabricated Gurugram intelligence.
- The AquaPulse Guide chatbot answers from the current prototype state and explicitly separates event hypotheses from pollution, safety and health conclusions.

## API highlights

- `GET /health`
- `GET /api/v1/intelligence/scenarios`
- `GET /api/v1/intelligence/run?scenario=rain_runoff`
- `GET /api/v1/intelligence/fingerprint?scenario=rain_runoff`
- `GET /api/v1/segments`
- `GET /api/v1/river-memory`
- `GET /api/v1/hot-moments`
- `GET /api/v1/verification`
- `POST /api/v1/verification`
- `GET /api/v1/citizen-reports`
- `POST /api/v1/citizen-reports`
- `GET /api/v1/evidence/overview`
- `GET /api/v1/evidence/cpcb`
- `GET /api/v1/data/rainfall/discover`

## Demo story — 3 to 5 minutes

1. Start on **Command Center**.
2. Explain the problem: a river can look normal while the combination of rainfall, environmental signals and historical patterns contains an earlier warning.
3. Click **Run demo**. Let the three scenario states cycle.
4. Pause on **Rain-amplified urban runoff** and point to the map, evidence mix and event fingerprint.
5. Open **River Memory** and show the historical resemblance.
6. Open **Hot Moments** and explain that this is a vulnerability window, not a certainty claim.
7. Open **Verification Centre** and show the prioritized locations.
8. Click **Confirm** on one location to demonstrate the human-in-the-loop workflow.
9. Open the **AquaPulse Guide** and ask “What is happening?” or “Where should I verify?” to demonstrate contextual, evidence-aware assistance.
10. Open **Evidence** and show the REAL / DERIVED / SIMULATED boundary.
11. Close with: **“AquaPulse does not wait for an environmental event to become obvious. It learns the moments when ecosystems become vulnerable.”**

## Hackathon alignment

Primary track: **Track 6 — Resilience Informatics**. Supporting alignment: **Track 2 — Data-to-Insight** and **Track 3 — AI-Supported Assessment**.

The OneAquaHealth IEEE Global Hackathon asks for a clear track alignment, project description, 3–5 minute demo video, public source repository and working prototype. The official page also states that judging considers impact/alignment, innovation, architecture, UX and scale. AquaPulse's submission materials should therefore make those five areas easy to verify.

Official hackathon page: https://oneaquahealth-ieee-hackathon.devpost.com/

## Responsible interpretation

- **Event confidence** is confidence in the event hypothesis, not a probability of toxicity or disease.
- **Potential impact** is a prioritization category, not a clinical or regulatory finding.
- **Evidence quality** describes support for the hypothesis.
- **Verification status** records human follow-up.
- **Propagation** is a network-prioritization heuristic, not a physical transport model.
- **CPCB** observations in this package are periodic/contextual.
- **NASA IMERG** is an official rainfall source; if retrieval is unavailable, AquaPulse reports that state instead of inventing a value.
- **Sentinel-2** is contextual and episodic rather than live high-frequency telemetry.
- Antibiotic-resistance genes and similar laboratory-only properties are scientific context/future verification targets, not outputs of the demo model.

## Submission checklist

Before submitting to Devpost, verify:

- [ ] Public GitHub repository contains this project and README.
- [ ] Demo video is 3–5 minutes and shows the working prototype.
- [ ] Devpost track is set to Track 6 — Resilience Informatics.
- [ ] Project description clearly states problem, solution, target users and expected impact.
- [ ] Real vs simulated data is disclosed.
- [ ] Screenshots/cover image are clear and readable.
- [ ] Team members are correctly listed.
- [ ] Repository runs from a clean checkout using the documented setup.
- [ ] Final submission is made before the official deadline.

## License / source note

This is a hackathon prototype. Third-party data and map services remain subject to their own terms, licenses and attribution requirements. OpenStreetMap attribution is displayed in the map.


### Backend test dependency
The smoke test uses FastAPI TestClient and therefore installs `httpx==0.28.1` from `backend/requirements.txt`.
