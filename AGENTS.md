# AGENTS.md

## Repo rules
- After any Python change, run:
  - `python -m compileall app migrations/versions`
  - `pytest -q`
- If tests fail because dependencies are missing, fix the environment first.
- Do not open a PR until the required checks pass.

## Setup
- Create/use the project environment.
- Install dependencies with:
  - `pip install -r requirements.txt`
  - `pip install Flask-Migrate pytest`

## Done when
- `python -m compileall app migrations/versions` passes
- `pytest -q` passes
- Summarize test output in the final response
