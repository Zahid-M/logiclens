import json
import random
from pathlib import Path

PUZZLES = json.loads(Path("puzzles.json").read_text())

FRAMINGS = ["neutral", "western", "diverse"]


class LogicLensEnv:
    """
    LogicLens: Name Framing Bias Benchmark

    Each episode presents one puzzle in one framing. The environment tracks
    which puzzle + framing was used so the scorer can group results by puzzle_id
    and measure consistency across the 3 framings.
    """

    def __init__(self, seed: int = 0):
        rng = random.Random(seed)
        puzzle = rng.choice(PUZZLES)
        framing = rng.choice(FRAMINGS)
        self.puzzle_id = puzzle["id"]
        self.puzzle_type = puzzle["type"]
        self.framing = framing
        self.correct_answer = puzzle["correct_answer"].split(" / ")[
            FRAMINGS.index(framing)
        ]
        self.question = puzzle["framings"][framing]
        self.done = False
        self.answer_given = None

    def reset(self):
        return {
            "observation": self.question,
            "metadata": {
                "puzzle_id": self.puzzle_id,
                "framing": self.framing,
                "type": self.puzzle_type,
            },
        }

    def step(self, action: str):
        self.done = True
        # Extract answer from last line if model uses ANSWER: format
        lines = [l.strip() for l in action.strip().splitlines() if l.strip()]
        raw = lines[-1] if lines else action.strip()
        if raw.upper().startswith("ANSWER:"):
            raw = raw[7:].strip()
        self.answer_given = raw.lower()
        correct = self.correct_answer.lower()

        is_correct = correct in self.answer_given or self.answer_given in correct

        return {
            "observation": f"Your answer: {raw}",
            "reward": 1.0 if is_correct else 0.0,
            "done": True,
            "info": {
                "puzzle_id": self.puzzle_id,
                "framing": self.framing,
                "correct_answer": self.correct_answer,
                "model_answer": raw,
                "is_correct": is_correct,
            },
        }
