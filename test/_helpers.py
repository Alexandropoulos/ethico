import json
from pathlib import Path

from ethico.evaluator import evaluate_dilemma

CASES_DIR = Path(__file__).resolve().parents[1] / "data" / "test_cases"


def case_files():
    files = sorted(CASES_DIR.glob("*/situation.json"))
    if not files:
        raise RuntimeError(f"No dilemma models found in {CASES_DIR}")
    return files


def situation_path(dilemma_name):
    path = CASES_DIR / dilemma_name / "situation.json"
    if not path.is_file():
        raise FileNotFoundError(f"Dilemma file missing: {path}")
    return path


def run_evaluation(dilemma_name, output_dir):
    source = situation_path(dilemma_name)
    output = output_dir / "evaluation.json"
    evaluate_dilemma(str(source), str(output))
    return json.loads(output.read_text(encoding="utf-8"))


def get_verdict(evaluation, theory):
    keys = {
        "kantian": "kantian_humanity_principle",
        "utilitarian": "utilitarian_principle",
    }
    verdict = evaluation[keys[theory]]["permissible"]
    assert type(verdict) is bool, f"Expected Boolean {theory} verdict, got {verdict!r}"
    return verdict
