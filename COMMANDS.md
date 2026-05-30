# LogicLens — Exact commands to run

Copy-paste these in order. Should take ~20 minutes.

## Step 1: Install & setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install swecc-mesocosm
```

## Step 2: Test locally (optional but good for the video)

```bash
# Terminal 1
python adapter.py

# Terminal 2
mesocosm run local --episodes 10
```

## Step 3: Push to GitHub

```bash
git init
git add .
git commit -m "Initial LogicLens benchmark"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/logiclens.git
git push -u origin main
```

## Step 4: Login and submit to Mesocosm platform

```bash
mesocosm auth login
mesocosm env submit \
  --name "LogicLens" \
  --github-url https://github.com/YOUR_USERNAME/logiclens \
  --description "Name framing bias benchmark for LLM reasoning consistency"
```

## Step 5: Run on the platform

```bash
mesocosm env list          # wait for status = ready, copy DOMAIN_ID

mesocosm run create \
  --domain DOMAIN_ID \
  --vow-version 1.0.0 \
  --model gemini/gemini-3.1-flash-lite \
  --episodes 60

mesocosm run create \
  --domain DOMAIN_ID \
  --vow-version 1.0.0 \
  --model YOUR_SECOND_MODEL \
  --episodes 60
```

## Step 6: Export and score results

```bash
mesocosm run export RUN_ID > results.json
python score.py results.json --verbose
```

## Step 7: Update the website

- Fill in real scores in `index.html` (the 4 model rows)
- Replace `YOUR_USERNAME`, `YOUR_VIDEO_URL`, `YOUR_DEVPOST_URL`
- Push changes to GitHub

## Step 8: Deploy website

Option A — GitHub Pages:
  - Repo Settings → Pages → Source: main branch, / (root)
  - Your site: https://YOUR_USERNAME.github.io/logiclens

Option B — Vercel (faster):
  - vercel.com → Import from GitHub → deploy
  - Done in 60 seconds

## Step 9: Record your video (90 seconds)

Script:
1. "Hi, we're [names], this is LogicLens built for SWECCathon 2026."
2. Show the showcase website briefly.
3. Show the terminal: `python adapter.py` in one tab, `mesocosm run local` in another.
4. "We're testing whether AI models give consistent answers to logic puzzles when names change."
5. Show the results page with real scores.
6. "Built with Mesocosm on SWECC's platform." Done.

Upload as unlisted YouTube video.

## Step 10: Submit Devpost

Required fields:
- Project name: LogicLens
- Tagline: Does a name change the answer?
- GitHub URL: https://github.com/YOUR_USERNAME/logiclens
- Website URL: your deployed index.html
- Video URL: your unlisted YouTube link
