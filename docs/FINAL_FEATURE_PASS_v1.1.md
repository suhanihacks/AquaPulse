# AquaPulse v1.1 — Final Feature Pass

This build freezes the product direction before full browser QA and Devpost packaging.

## Seven final refinements

1. **One Health impact layer** — makes the ecosystem/community/human-well-being connection explicit without making clinical claims.
2. **How AquaPulse Reasons** — visualizes signal fusion → event hypothesis → human verification priority.
3. **Prototype boundary** — high-frequency event scenarios are clearly labelled simulated; contextual external sources retain provenance labels.
4. **Gurugram preview** — demonstrates city scalability without fabricating local intelligence where validated datasets are not connected.
5. **Demo hardening** — scenario refreshes preserve the current rendered view while intelligence updates, reducing white-screen transitions and stale-response races.
6. **Navigation/UX hardening** — city dropdown click-away/Escape handling, compact map sizing, update state, and resilient section rendering.
7. **AquaPulse Guide chatbot** — an in-product, evidence-aware contextual assistant that explains the current event, evidence, River Memory, Hot Moments, provenance, One Health and verification priorities. It does not claim live telemetry, pollution diagnosis, drinking-water safety, disease diagnosis, or laboratory detection.

## Important implementation note

The AquaPulse Guide is intentionally self-contained for the hackathon prototype. It uses the current AquaPulse state and bounded intent responses, so the demo does not depend on an external LLM API key or network availability. A production version can replace the response layer with a validated retrieval/LLM service while preserving the same provenance and safety guardrails.
