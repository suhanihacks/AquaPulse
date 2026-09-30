# AquaPulse — Final Build Checklist

## Runtime
- [x] Backend is FastAPI and targets CPython 3.12.x on Windows 11.
- [x] Frontend is React + Vite and uses pinned package versions.
- [x] `run_backend.ps1` creates/activates the Python environment and starts port 8000.
- [x] `run_frontend.ps1` installs frontend dependencies if needed and starts Vite on port 5173.
- [x] Frontend API URL can be overridden with `VITE_API_BASE_URL`.

## Product
- [x] Command Center
- [x] Interactive river map
- [x] Event confidence and evidence mix
- [x] Event fingerprinting
- [x] River Memory
- [x] Hot Moment intelligence
- [x] Verification Centre
- [x] Citizen observation input
- [x] Evidence & provenance page
- [x] Guided demo mode
- [x] One Health impact framing
- [x] Explainable 'How AquaPulse Reasons' panel
- [x] Honest Gurugram platform preview with no fabricated local intelligence
- [x] Hardened scenario refresh/navigation behavior to reduce white-screen states
- [x] AquaPulse Guide contextual chatbot with bounded, evidence-aware answers
- [x] Responsive layout and visible text hierarchy

## Scientific / responsible-AI guardrails
- [x] Real, derived and simulated data are explicitly separated.
- [x] CPCB records are described as contextual/historical, not live telemetry.
- [x] NASA IMERG is not fabricated when unavailable.
- [x] Sentinel-2 is contextual/episodic, not claimed as live high-frequency telemetry.
- [x] Rainfall alone is prevented from becoming a strong event claim.
- [x] The intelligence output is an event hypothesis, not a pollution/health diagnosis.
- [x] Propagation is a graph-based prioritization heuristic, not a hydrodynamic contaminant-transport model.
- [x] Human verification remains the final decision step.
- [x] Chatbot explicitly avoids pollution, drinking-water safety and health-diagnosis claims.

## Hackathon submission alignment
- [x] Primary track: Track 6 — Resilience Informatics.
- [x] Supporting tracks: Track 2 — Data-to-Insight and Track 3 — AI-Supported Assessment.
- [x] Problem, target users, solution and expected impact documented.
- [x] Prototype/demo workflow documented.
- [x] Public-repository-ready source tree.
- [x] Demo-video storyboard included in README.

## Final testing phase
The included `tests_smoke.py` is a backend smoke test. Full local validation should be performed after extraction on the target Windows machine, including frontend installation/build, browser interaction, map tiles, scenario switching, citizen reports, verification actions, refresh behavior and offline/error states.


## Final dependency note
The backend smoke test uses FastAPI TestClient, which requires `httpx`; `httpx==0.28.1` is pinned in `backend/requirements.txt`.
