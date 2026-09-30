@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Root .venv not found. Run: py -3.12 -m venv .venv
  exit /b 1
)
.venv\Scripts\python.exe tests_smoke.py
endlocal
