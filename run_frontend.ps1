$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
Set-Location (Join-Path $root "frontend")

if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js is required. Install Node.js 20.19+ (or Node 22.12+) and reopen VS Code." }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw "npm is required. Install Node.js 20.19+ (or Node 22.12+) and reopen VS Code." }

npm install
npm run dev
