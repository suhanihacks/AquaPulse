$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { throw "Root .venv not found. Run: py -3.12 -m venv .venv" }
& $python (Join-Path $root "tests_smoke.py")
