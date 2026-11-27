import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from test._helpers import run_evaluation


def main():
    parser = argparse.ArgumentParser(description="Evaluate a reference dilemma.")
    parser.add_argument("dilemma_name", help="Case directory name, e.g. trolley_problem")
    args = parser.parse_args()

    with TemporaryDirectory() as directory:
        result = run_evaluation(args.dilemma_name, Path(directory))
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
