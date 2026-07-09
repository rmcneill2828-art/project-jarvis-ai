@echo off
REM Bootstraps a fresh clone of Project JARVIS AI for local development.
REM Double-click this file, or run it from a terminal.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup-dev-environment.ps1"
pause
