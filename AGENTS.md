# Study OS — Agent Guide

## Repository

- **Remote:** `origin` → https://github.com/adiStudent-in/Commerce.git
- **Branch:** `master`
- **Website source:** `Webpage/` (entry point: `Webpage/index.html`)
- **Local preview:** run a static server from `Webpage/`, e.g. `python -m http.server 8765`

## Push policy — important

- **Never push without the user's explicit permission.**
- Finish and verify website changes first. Do not push in the middle of a task.
- At the end of each batch of website changes, ask the user once whether to commit and push to `origin/master`.
- Only ask at the end, when the work is complete — not repeatedly mid-task.
- Before pushing, state exactly which changes will be committed.
- Do not include unrelated pending changes in a commit without the user's approval.
- If permission is not given, leave the changes local and uncommitted.

## Project notes

- The site is a static Class XI Commerce study hub with subject chapters, a dashboard, a syllabus tracker, and PWA support.
- Shared website assets live in `Webpage/assets/`.
- PWA metadata: `Webpage/manifest.json`; cache version: `Webpage/service-worker.js`.
- Keep generated mirrors (`.playwright-cli/`, browser screenshots) out of commits.
