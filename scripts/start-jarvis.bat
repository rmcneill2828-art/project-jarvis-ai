@echo off
REM Start JARVIS Guardian Desktop Shell - double-click launcher.
REM Runs the same "npm run tauri dev" path validated live at ESR-0025.
REM
REM Conversations are answered by a local Ollama instance (start Ollama first).
REM To allow Claude as a confirmed-escalation provider, set ANTHROPIC_API_KEY as a
REM persistent Windows user environment variable first (System Properties ->
REM Environment Variables -> New, under "User variables") - never paste a key
REM directly into this file, since it is not something you want committed or
REM shared by accident.

cd /d "%~dp0.."
call npm run tauri dev
