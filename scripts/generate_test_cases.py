import shutil
import sys
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
ENGINE_DIR = ROOT / "ethics_engine"
CASES_DIR = ENGINE_DIR / "cases"
OUTPUT_DIR = ROOT / "data" / "test_cases"

# Make both packages importable
sys.path.insert(0, str(ROOT))
sys.path.insert(1, str(ENGINE_DIR))

# Import only after configuring sys.path
from ethico.evaluator import evaluate_dilemma


def generate_test_cases():
    if not CASES_DIR.is_dir():
        raise FileNotFoundError(
            f"Cases directory not found: {CASES_DIR}"
        )

    case_files = sorted(CASES_DIR.glob("*.json"))

    if not case_files:
        print(f"No JSON cases found in {CASES_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    succeeded = 0
    failed = []

    for case_file in case_files:
        case_dir = OUTPUT_DIR / case_file.stem
        case_dir.mkdir(parents=True, exist_ok=True)

        situation_path = case_dir / "situation.json"
        evaluation_path = case_dir / "evaluation.json"

        # Copy the original situation without modifications.
        shutil.copy2(case_file, situation_path)

        try:
            evaluate_dilemma(
                str(situation_path),
                str(evaluation_path),
            )
            succeeded += 1
            print(f"[OK] {case_file.stem}")

        except (OSError, ValueError, KeyError, RuntimeError) as exc:
            # Avoid retaining an evaluation from a previous run.
            evaluation_path.unlink(missing_ok=True)

            failed.append((case_file.name, str(exc)))
            print(f"[FAILED] {case_file.name}: {exc}")

    print("\nGeneration summary")
    print(f"Total cases: {len(case_files)}")
    print(f"Successful:  {succeeded}")
    print(f"Failed:      {len(failed)}")

    if failed:
        print("\nFailed cases:")
        for filename, error in failed:
            print(f"  - {filename}: {error}")


if __name__ == "__main__":
    generate_test_cases()
