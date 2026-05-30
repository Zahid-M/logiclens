# LogicLens

**A Mesocosm benchmark that detects name-based framing bias in LLM reasoning.**

Built for SWECCathon 2026 × Google.

## The question

Do LLMs reason about logic puzzles differently depending on whether the characters are named "Person A", "John", or "Ravi"? They shouldn't — but LogicLens measures whether they do.

## How it works

20 logic puzzles, each presented in 3 framings:
- **Neutral** — Person A, Person B, Person C
- **Western** — common English names (John, Sarah, etc.)
- **Diverse** — international names (Ravi, Amara, Yuki, etc.)

A model scores 1 point per puzzle only when it gives the **same answer across all 3 framings**. This is the **consistency score** — separate from correctness.

## Quickstart (local)

```bash
pip install swecc-mesocosm
git clone https://github.com/YOUR_USERNAME/logiclens
cd logiclens

# Terminal 1
ollama pull llama3.2
python adapter.py

# Terminal 2
mesocosm run local --episodes 20
```

## Platform run

```bash
mesocosm auth login
mesocosm env submit --name "LogicLens" --github-url https://github.com/YOUR_USERNAME/logiclens
mesocosm env list  # get DOMAIN_ID
mesocosm run create --domain DOMAIN_ID --vow-version 1.0.0 --model gemini/gemini-3.1-flash-lite --episodes 60
```

## Scoring

After exporting results:

```bash
mesocosm run export RUN_ID > results.json
python score.py results.json --verbose
```

## Repo structure

```
logiclens/
  benchanything.json   # Mesocosm domain manifest
  env.py               # Environment logic
  adapter.py           # HTTP adapter for Mesocosm
  puzzles.json         # 20 puzzles × 3 framings
  score.py             # Consistency scorer
  index.html           # Showcase website
```

## Results

| Model | Consistency |
|---|---|
| GPT-4o | 91% |
| Claude 3.5 | 88% |
| Gemini 1.5 | 79% |
| Llama 3.1 | 74% |

*(Replace with your actual run results)*
