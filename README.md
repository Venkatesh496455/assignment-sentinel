# 🛡️ Assignment Sentinel

AI-powered code review for GitHub pull requests — built to help student developers get instant, structured feedback before a human ever looks at their code.

## What it does

Assignment Sentinel connects to any GitHub pull request, analyzes the diff using Google's Gemini API, and returns a structured, deterministic score (not just an AI opinion) broken down by issue severity. It runs three ways:

- **CLI** — review any PR from your terminal
- **Web dashboard** — a React interface to review any repo/PR interactively
- **GitHub Actions bot** — automatically reviews and comments on every new pull request

## Why it's different

Most "AI code reviewer" projects let the AI freely assign a score, which produces inconsistent results — a typo and a security leak can get penalized similarly. Assignment Sentinel instead has the AI **only classify issues by severity** (critical / major / minor), while a **deterministic Python scoring engine** calculates the final score and grade. This keeps scoring consistent and explainable, and is fully unit-tested.

## Tech stack

- **Backend:** Python, FastAPI
- **Frontend:** React (Vite)
- **AI:** Google Gemini API (`gemini-2.5-flash`)
- **Automation:** GitHub Actions
- **Testing:** pytest

## Screenshots

*(add screenshots of the dashboard and a PR comment here)*

## How it works

1. Fetches the real diff of a pull request via the GitHub REST API
2. Sends the diff to Gemini with a structured prompt requesting categorized issues
3. A custom scoring engine (`calculate_score()`) deducts weighted points per issue severity:
   - Critical: -3.0 | Major: -1.5 | Minor: -0.5
4. Returns a score (0–10), letter grade (A–F), and categorized breakdown

## Running locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
Create a `.env` file in `backend/`:
```
GEMINI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
```

Run the API:
```bash
python -m uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Run tests
```bash
cd backend
python -m pytest test_core.py -v
```

## Automated PR reviews

This repo includes a GitHub Actions workflow (`.github/workflows/pr-review.yml`) that automatically reviews every new pull request and posts the results as a comment. To use it in your own repo, add `GEMINI_API_KEY` as a repository secret.

## Roadmap

- [ ] Deploy backend + frontend so the dashboard is publicly usable
- [ ] Support reviewing full repos, not just individual PRs
- [ ] Add AI-suggested project/skill improvement recommendations

## License

MIT
