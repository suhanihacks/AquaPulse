@echo off
setlocal
cd /d "%~dp0frontend"
where node >nul 2>&1 || (echo Node.js is required. Install Node.js 20.19+ or Node.js 22.12+ and reopen VS Code. & exit /b 1)
where npm >nul 2>&1 || (echo npm is required. Install Node.js 20.19+ or Node.js 22.12+ and reopen VS Code. & exit /b 1)
npm install || exit /b 1
npm run dev
endlocal
