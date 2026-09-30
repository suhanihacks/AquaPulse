# AquaPulse Final Validation Notes

## Backend

The backend smoke suite was executed against the packaged project and passed all expected checks. The intentional unknown-scenario case returns HTTP 404.

Checked endpoints include:

- health
- three intelligence scenarios
- unknown scenario guard
- segments
- River Memory
- Hot Moments
- Verification GET/POST
- Evidence
- CPCB
- data overview
- rainfall demo features
- citizen report POST

## Frontend source hardening

The final UI pass includes:

- section navigation with active state, URL hash support and scroll-to-top behavior
- Demo Mode pauses when the user changes section
- Dehradun-only study-area selector with transparent future-city state
- Leaflet `invalidateSize` handling after render and resize
- visible action errors for citizen-report and verification failures
- keyboard focus-visible styling for interactive controls
- sticky section navigation for long pages

## Data integrity

High-frequency event scenarios remain clearly simulated. CPCB data remains contextual historical evidence. The application does not fabricate unavailable NASA rainfall retrievals.

## Frontend build note

A production frontend build must be confirmed in the user's Windows/Node environment after `npm install`. The development server has already been demonstrated locally by the user at `http://127.0.0.1:5173`.
