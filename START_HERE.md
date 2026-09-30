# AquaPulse — Start Here

This is the single final build. **Do not create a separate Python environment inside `backend/`.**
Use one `.venv` at the project root.

## Windows 11 + VS Code

### 1. Backend environment
Open PowerShell in the folder that contains `README.md` and `backend/`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

PowerShell activation is **not required**.

### 2. Backend smoke test

```powershell
.\.venv\Scripts\python.exe tests_smoke.py
```

Expected final line:

```text
AquaPulse backend smoke test: PASS
```

### 3. Start backend

**Recommended on Windows:**

```powershell
.\run_backend.cmd
```

Open:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

### 4. Start frontend
Open a second VS Code terminal:

```powershell
.\run_frontend.cmd
```

Or manually:

```powershell
cd frontend
npm install
npm run dev
```

Open:
- http://127.0.0.1:5173

### 5. Navigation and study area

The top section navigation is interactive and supports direct section URLs such as `#memory`, `#hot`, `#verify`, and `#evidence`. Selecting a section returns the page to the top and pauses Demo Mode so the selected view stays stable.

The current validated study area is **Dehradun**. The study-area selector is intentionally prepared for additional cities, but unvalidated cities are not enabled yet. A future public platform can add a city only after its datasets, geometry, evidence registry and model configuration are connected.

### 6. PowerShell note

Windows may block unsigned `.ps1` launchers extracted from downloaded ZIPs because of its file-origin security policy. **Use the `.cmd` launchers above** or the manual commands; do not change the system execution policy globally just for AquaPulse.

## Important provenance rule

The prototype labels `REAL`, `DERIVED`, and `SIMULATED` evidence explicitly. High-frequency event signals and citizen reports in the demo are simulated; bundled CPCB records are contextual historical evidence. AquaPulse does not claim live pollution, toxicity, ARG, or laboratory detection from these demo signals.
