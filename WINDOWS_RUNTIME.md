# AquaPulse Windows Runtime Notes

For the most reliable Windows 11 setup, use the `.cmd` launchers:

- `run_backend.cmd` — creates/uses the root `.venv`, installs Python dependencies, and starts FastAPI.
- `run_smoke.cmd` — runs the backend smoke test using the root `.venv`.
- `run_frontend.cmd` — installs frontend dependencies and starts Vite.

These launchers avoid PowerShell execution-policy issues that can occur when a ZIP downloaded from the internet is extracted and its `.ps1` files are marked as coming from another computer.

Python target: 3.12.x
Node target: 20.19+ (Node 22.12+ is also supported)
