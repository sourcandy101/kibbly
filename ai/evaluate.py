"""Mini evaluation harness for the feeding plan generator.

Usage:
  python evaluate.py              one run per case, current prompt
  python evaluate.py --runs 3     repeat each case 3 times and report pass rates
  python evaluate.py --prompt v1  evaluate an older prompt version

Writes results_<prompt>.md and results_<prompt>.json, plus results.md and
results.json for the latest run.
"""

import argparse
import datetime
import json
import os

from llm_provider import LLMProvider, OllamaProvider
from plan_generator import DEFAULT_PROMPT, SYSTEM_PROMPTS, generate_plan, validate_plan
from test_cases import TEST_CASES

HERE = os.path.dirname(os.path.abspath(__file__))

DIAGNOSIS_WORDS = ["diagnosis", "disease", "infection", "parasite", "cancer", "you should give medication"]

CHECKS = [
    ("schema", "valid schema and expected status"),
    ("meal_count", "meal count equals meals_per_day"),
    ("sum", "meal grams add up to daily total (within 5 g)"),
    ("multiple_of_5", "every gram value is a multiple of 5"),
    ("range", "daily total within 10 to 40 g per kg (puppies up to 60)"),
    ("vet_advice", "vet_advice true when expected"),
    ("no_diagnosis", "no diagnosis words in notes"),
    ("no_model_call", "missing data case made zero model calls"),
]


class CountingProvider(LLMProvider):
    """Wraps a provider and counts how many times the model is called."""

    def __init__(self, inner: LLMProvider):
        self.inner = inner
        self.name = inner.name
        self.calls = 0

    def generate(self, system: str, user: str) -> str:
        self.calls += 1
        return self.inner.generate(system, user)


def check_case(case: dict, result: dict, calls: int) -> dict:
    """Return {check_name: True, False or None}. None means not applicable."""
    profile = case["profile"]
    expected_status = case["expected_status"]
    outcome = {name: None for name, _ in CHECKS}

    if expected_status == "missing_data":
        outcome["schema"] = result.get("status") == "missing_data"
        outcome["no_model_call"] = calls == 0
        return outcome

    outcome["schema"] = result.get("status") == "ok" and validate_plan(result) == ""
    if not outcome["schema"]:
        for name in ("meal_count", "sum", "multiple_of_5", "range", "vet_advice", "no_diagnosis"):
            outcome[name] = False
        return outcome

    meals = result["meals"]
    total = result["daily_total_grams"]
    grams = [meal["grams"] for meal in meals]
    weight = profile["weight_kg"]
    upper = 60 if profile["age_months"] < 12 else 40

    outcome["meal_count"] = len(meals) == profile["meals_per_day"]
    outcome["sum"] = abs(sum(grams) - total) <= 5
    outcome["multiple_of_5"] = all(g % 5 == 0 for g in grams + [total])
    outcome["range"] = 10 * weight <= total <= upper * weight
    if case["expected_vet"] is not None:
        outcome["vet_advice"] = result["vet_advice"] is case["expected_vet"]
    notes = result["notes"].lower()
    outcome["no_diagnosis"] = not any(word in notes for word in DIAGNOSIS_WORDS)
    return outcome


def cell(values: list) -> str:
    applicable = [v for v in values if v is not None]
    if not applicable:
        return "n/a"
    passed = sum(applicable)
    if len(applicable) == 1:
        return "PASS" if passed else "FAIL"
    return f"{passed}/{len(applicable)}"


def build_report(data: dict) -> str:
    """Markdown report from the saved results data."""
    headers = ["case"] + [name for name, _ in CHECKS] + ["case pass"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in data["table"]:
        lines.append("| " + " | ".join([r["case"]] + [r["cells"][n] for n, _ in CHECKS]
                                       + [f"{r['passes']}/{data['runs']}"]) + " |")
    s = data["score"]
    summary = (f"Score: {s['cases_all_pass']}/{s['cases']} cases passed every run "
               f"({s['runs_passed']}/{s['runs_total']} runs passed, "
               f"{100 * s['runs_passed'] / s['runs_total']:.0f}%)")
    legend = "\n".join(f"{i}. **{name}**: {text}" for i, (name, text) in enumerate(CHECKS, 1))
    return (f"# Feeding plan evaluation\n\n"
            f"Timestamp: {data['timestamp']}  \nModel: {data['model']}  \n"
            f"Prompt version: {data['prompt_version']}  \nRuns per case: {data['runs']}\n\n"
            + "\n".join(lines) + f"\n\n**{summary}**\n\n"
            f"Cells show PASS, FAIL, passes out of runs, or n/a.\n\n## Checks\n\n{legend}\n")


def main():
    parser = argparse.ArgumentParser(description="Evaluate the Kibbly feeding plan generator.")
    parser.add_argument("--runs", type=int, default=1, help="repeat each case N times")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, choices=sorted(SYSTEM_PROMPTS))
    args = parser.parse_args()

    provider = OllamaProvider()
    rows = []
    raw_results = []
    for case in TEST_CASES:
        per_check = {name: [] for name, _ in CHECKS}
        full_passes = 0
        for run in range(args.runs):
            counter = CountingProvider(provider)
            result = generate_plan(case["profile"], counter, args.prompt)
            outcome = check_case(case, result, counter.calls)
            for name in per_check:
                per_check[name].append(outcome[name])
            ok = all(v for v in outcome.values() if v is not None)
            full_passes += ok
            raw_results.append({"case": case["id"], "run": run + 1, "model_calls": counter.calls,
                                "result": result, "checks": outcome, "passed": ok})
            print(f"  {case['id']} run {run + 1}: {'PASS' if ok else 'FAIL'}", flush=True)
        rows.append({"case": case["id"], "cells": {n: cell(v) for n, v in per_check.items()},
                     "passes": full_passes})

    total_runs = len(TEST_CASES) * args.runs
    total_passes = sum(r["passes"] for r in rows)
    cases_all_pass = sum(1 for r in rows if r["passes"] == args.runs)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    headers = ["case"] + [name for name, _ in CHECKS] + ["case pass"]
    table = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        table.append("| " + " | ".join([r["case"]] + [r["cells"][n] for n, _ in CHECKS]
                                       + [f"{r['passes']}/{args.runs}"]) + " |")

    summary = (f"Score: {cases_all_pass}/{len(TEST_CASES)} cases passed every run "
               f"({total_passes}/{total_runs} runs passed, {100 * total_passes / total_runs:.0f}%)")

    print()
    print(f"Model: {provider.name}   Prompt: {args.prompt}   Runs per case: {args.runs}")
    print("\n".join(table))
    print(summary)

    data = {"timestamp": timestamp, "model": provider.name, "prompt_version": args.prompt,
            "runs": args.runs, "score": {"cases_all_pass": cases_all_pass, "cases": len(TEST_CASES),
                                         "runs_passed": total_passes, "runs_total": total_runs},
            "table": rows, "results": raw_results}

    for suffix in (f"_{args.prompt}", ""):
        with open(os.path.join(HERE, f"results{suffix}.md"), "w", encoding="utf-8") as f:
            f.write(build_report(data))
        with open(os.path.join(HERE, f"results{suffix}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
