# Development Environment Baseline

Software required to build and run Project JARVIS AI (a Tauri desktop app: Rust backend, React/Vite frontend, Python tooling) on a new machine.

| Tool | Why it's needed | Minimum version |
|---|---|---|
| [Git](https://git-scm.com/download/win) | clone the repo; the tracked pre-commit hook runs through it | any recent |
| [Node.js LTS](https://nodejs.org/) (includes npm) | builds/runs the React/Vite frontend (`npm install`, `npm run dev`/`build`) | 18+ (LTS) |
| [Rust toolchain](https://rustup.rs/) (rustup + cargo) | builds the Tauri/Rust backend (`cargo build`) | stable |
| [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) ("Desktop development with C++" workload) | MSVC linker required by the Rust build on Windows | - |
| [WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/) | renders the Tauri UI; usually preinstalled on Windows 10 21H2+/11 | - |
| [Python](https://www.python.org/downloads/) | `.venv`, `ruff`, `pytest`, the repository validator | 3.12+ |

## Checking a machine

Run:

```text
scripts\check-prerequisites.ps1
```

It checks every tool above and, if `winget` is available, offers to install anything missing. `setup.bat` runs this automatically as its first step, so on a new laptop you can just run `setup.bat` directly.

If a tool was just installed via winget, the script refreshes `PATH` for the current session where it can; if a tool still isn't detected afterwards, close and reopen your terminal and re-run `setup.bat`.
