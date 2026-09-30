# AquaPulse — OneAquaHealth Submission Alignment

## Team
- Suhani Goel
- Ishika Bansal

## Project
**AquaPulse — Freshwater Event Intelligence**

## Primary track
**Track 6 — Resilience Informatics**

## Supporting alignment
- Track 2 — Data-to-Insight
- Track 3 — AI-Supported Assessment

## Problem
Urban freshwater systems can experience short-lived environmental stress events that are difficult to interpret from isolated observations. Communities and field teams need a way to combine environmental context, citizen observations and historical patterns into an actionable investigation workflow.

## Solution
AquaPulse is an explainable event-intelligence prototype that fuses multiple evidence streams, identifies event signatures, compares them with River Memory, highlights vulnerable windows, projects downstream verification candidates and keeps a human verifier in the loop.

## Target users
- Environmental monitoring teams
- Researchers and citizen-science coordinators
- Local resilience / water-management stakeholders
- Communities contributing observations

## One Health connection
The system is designed around the connection between ecosystem condition, biodiversity/environmental health and human/community well-being. It does not make clinical or laboratory claims from insufficient evidence.

## What judges can see in the prototype
1. Multi-signal event confidence
2. Explainable evidence mix
3. Event fingerprinting
4. River Memory similarity
5. Hot Moment vulnerability score
6. Geospatial propagation/prioritization
7. Verification Centre
8. Citizen observation input
9. REAL / DERIVED / SIMULATED provenance
10. Guided demonstration mode
11. AquaPulse Guide contextual chatbot
12. One Health impact framing and explainable reasoning panel

## Architecture evidence
- React + Vite frontend
- FastAPI backend
- Leaflet/OpenStreetMap map
- Python data/intelligence layer
- CPCB contextual evidence
- NASA GPM IMERG adapter
- Sentinel-2 contextual registry
- Explicit simulation boundary for unavailable high-frequency telemetry
- Contextual in-product chatbot using the current event state; no external LLM dependency required for the demo

## Responsible-AI position
AquaPulse is an **AI-assisted decision-support prototype**, not an autonomous environmental or health authority. The AquaPulse Guide is intentionally evidence-aware and bounded: it explains the prototype state, provenance and next actions rather than fabricating live observations or making health/safety diagnoses. It produces event hypotheses, uncertainty-aware evidence and verification priorities. Human field verification remains the final step.

## Demo video structure — target 3–5 minutes
- 0:00–0:30 — problem and One Health context
- 0:30–1:20 — Command Center + map
- 1:20–2:00 — guided event scenarios
- 2:00–2:35 — River Memory + Hot Moments
- 2:35–3:20 — Verification Centre + citizen observation
- 3:20–3:50 — Evidence & provenance
- 3:50–4:20 — architecture/scalability + closing message
