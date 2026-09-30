# AquaPulse UI QA refinement

This pass preserves the existing visual design and focuses on reliability and clarity.

## Changes
- Section navigation now presents each section as a distinct view instead of leaving the Command Center hero/scenario shell above every page.
- Added a React error boundary around section content so a component error presents a recoverable UI instead of a blank screen.
- Added a subtle section transition.
- Demo Mode pauses automatically when a user navigates to another section.
- Study-area selector is kept intentionally honest: Dehradun is the only validated active study area; additional cities are shown as future expansion until validated local datasets are connected.
- Header layout is now non-wrapping so the study-area chevron and controls remain aligned.
- Renamed the provenance badge to `DEMO DATA · SIMULATED SIGNALS` and added an explanatory tooltip.
- Reduced the map height and explicitly synchronized the Leaflet container height to remove the oversized blank area below the map.
- Expanded citizen observations with oil sheen, sewage smell, floating waste, algae/green water, plus a custom observation field.
- Successful citizen reports now show the exact observation submitted.
- Refresh has a clear tooltip explaining that it refreshes the current intelligence view.

## Validation
- Python backend compilation: PASS.
- Backend smoke suite: PASS (health, three scenarios, invalid scenario, segments, memory, hot moments, verification, evidence, CPCB, data overview, rainfall features, citizen report, verification action).
- Frontend production build was not executed in this environment because npm registry access is unavailable here. The user's Windows environment is the final frontend build/runtime check.


## Platform navigation and city preview refinement
- Navigation uses URL hash anchors for reliable section switching and active-state rendering.
- Demo mode stops when changing sections.
- Study-area control is vertically aligned and uses a dedicated chevron icon.
- Added Gurugram (Gurgaon) as a preview-only city. No freshwater intelligence is generated for it until validated local datasets are connected.
- Gurugram preview shows geographic context without reusing Dehradun event data.
- Dehradun remains the only validated intelligence study area in the current prototype.
