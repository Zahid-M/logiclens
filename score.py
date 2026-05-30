"""
LogicLens scorer — run after mesocosm run export to compute consistency scores.

Usage:
    python score.py results.json
    python score.py results.json --verbose
"""

import json
import sys
from collections import defaultdict


def load_results(path: str) -> list[dict]:
    with open(path) as f:
        data = json.load(f)
    # Handle both raw list or wrapped {"episodes": [...]}
    if isinstance(data, list):
        return data
    return data.get("episodes", data.get("results", []))


def score(results: list[dict], verbose: bool = False):
    # Group by (model, puzzle_id)
    groups: dict[tuple, dict] = defaultdict(lambda: defaultdict(list))

    for ep in results:
        info = ep.get("info", {})
        model = ep.get("model", "unknown")
        puzzle_id = info.get("puzzle_id", ep.get("puzzle_id", "?"))
        framing = info.get("framing", ep.get("framing", "?"))
        answer = info.get("model_answer", ep.get("model_answer", "")).lower().strip()
        groups[model][puzzle_id].append({"framing": framing, "answer": answer})

    print("\n=== LogicLens Consistency Scores ===\n")

    for model, puzzles in sorted(groups.items()):
        consistent = 0
        total = 0
        framing_pairs = []

        for puzzle_id, episodes in puzzles.items():
            if len(episodes) < 2:
                continue
            answers = [e["answer"] for e in episodes]
            is_consistent = len(set(answers)) == 1
            consistent += int(is_consistent)
            total += 1

            if verbose:
                mark = "✓" if is_consistent else "✗"
                framing_pairs.append(
                    f"  Puzzle {puzzle_id:>2} {mark}  "
                    + "  |  ".join(f"{e['framing']}: '{e['answer']}'" for e in episodes)
                )

        pct = (consistent / total * 100) if total else 0
        print(f"Model: {model}")
        print(f"  Consistency: {consistent}/{total} puzzles ({pct:.1f}%)")

        if verbose:
            for line in framing_pairs:
                print(line)
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python score.py results.json [--verbose]")
        sys.exit(1)

    path = sys.argv[1]
    verbose = "--verbose" in sys.argv
    results = load_results(path)
    score(results, verbose=verbose)
