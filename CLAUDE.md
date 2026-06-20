# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running Locally

```bash
pip install -r requirements.txt
flask --app api/index.py run
```

The app runs on `http://localhost:5000` by default.

## Architecture

This is a Japanese personality quiz app ("ココメ診断") built with Flask and deployed to Vercel.

**Entry point:** `api/index.py` — the Flask app. Vercel routes all traffic here via `vercel.json`. The app has two routes:
- `GET /` — renders `templates/index.html` (quiz form with 3 yes/no questions)
- `POST /result` — sums scores from `q1`, `q2`, `q3` and renders `templates/result.html` with a `result_type` string

**Scoring logic** (in `api/index.py`): each question contributes 0 or 1 to a total score (max 3). The score maps to one of five personality types: `cocome_fuwafuwa`, `cocome_majime`, `cocome_tension`, `cocome_tsundere`, `cocome_uranai`.

**Static assets:** `A.png`, `B.png`, `C.png` are character images likely used in result display. `static/` and `templates/` are referenced by Flask but currently empty/placeholder.

**`app.py`** at root is a placeholder and not used — the real app is `api/index.py`.

**`ramen_story.html`** is a standalone animated story page (Japanese ramen shop narrative), not connected to the quiz app.

## Deployment

Deployed on Vercel. `vercel.json` points all routes to `api/index.py` using `@vercel/python`. Push to `main` to deploy.
