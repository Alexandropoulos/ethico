import glob
import json
import os
import re
import sys

from deepeval.test_case import ConversationalTestCase, LLMTestCase, Turn


def load_test_cases(experiments_dir, input_file, output_file):
    test_cases = []

    for folder_name in os.listdir(experiments_dir):
        folder_path = os.path.join(experiments_dir, folder_name)
        input_path = os.path.join(folder_path, input_file)
        output_path = os.path.join(folder_path, output_file)

        if (
            not os.path.isdir(folder_path)
            or not os.path.exists(input_path)
            or not os.path.exists(output_path)
        ):
            continue

        with open(input_path, encoding="utf-8") as file:
            input_text = file.read().strip()

        with open(output_path, encoding="utf-8") as file:
            output_text = file.read().strip()

        test_cases.append(
            LLMTestCase(
                input=input_text,
                actual_output=output_text,
                name=folder_name,
            )
        )

    return test_cases


def run_evaluation(test_cases, metrics, output_path):
    if not test_cases:
        print("No test cases found. Halting evaluation.")
        sys.exit(1)

    print(f"Starting evaluation on {len(test_cases)} test cases...")
    results = []

    for test_case in test_cases:
        name, case_obj = (
            test_case if isinstance(test_case, tuple) else (test_case.name, test_case)
        )

        print(f"\n{name}")
        case = {"name": name, "passed": True, "metrics": []}

        for metric in metrics:
            metric.measure(case_obj)
            passed = metric.is_successful()
            case["passed"] = case["passed"] and passed
            metric_name = getattr(metric, "name", metric.__class__.__name__)

            print(
                f"  {'✅' if passed else '❌'} {metric_name}: "
                f"{metric.score:.3f} - {metric.reason}"
            )

            case["metrics"].append(
                {
                    "metric": metric_name,
                    "score": round(metric.score, 3),
                    "threshold": metric.threshold,
                    "passed": passed,
                    "reason": metric.reason,
                }
            )

        results.append(case)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print(f"\n📄 Saved to {output_path}")


def create_conversational_test_case(
    file_path: str,
) -> tuple[str, ConversationalTestCase]:
    """Parses a single extraction.txt file into a ConversationalTestCase."""
    source_pattern = re.compile(r"\\s*")

    with open(file_path, encoding="utf-8") as file:
        lines = file.readlines()

    turns = []
    current_role = None
    current_content = ""

    for line in lines:
        clean_line = source_pattern.sub("", line).strip()

        if not clean_line:
            continue

        if clean_line.lower().startswith("user:"):
            if current_role and current_content:
                turns.append(Turn(role=current_role, content=current_content.strip()))

            current_role = "user"
            current_content = clean_line[5:].strip() + "\n"

        elif clean_line.lower().startswith("assistant:"):
            if current_role and current_content:
                turns.append(Turn(role=current_role, content=current_content.strip()))

            current_role = "assistant"
            current_content = clean_line[10:].strip() + "\n"

        elif current_role:
            current_content += clean_line + "\n"

    if current_role and current_content:
        turns.append(Turn(role=current_role, content=current_content.strip()))

    return (
        os.path.basename(os.path.dirname(file_path)),
        ConversationalTestCase(turns=turns),
    )


def load_conversational_test_cases(
    glob_pattern: str,
) -> list[tuple[str, ConversationalTestCase]]:
    """Finds all files matching the pattern and returns a list of test cases."""
    test_cases = []
    file_paths = glob.glob(glob_pattern)

    print(f"Found {len(file_paths)} files matching the pattern.")

    for file_path in file_paths:
        try:
            test_case = create_conversational_test_case(file_path)

            if test_case[1].turns:
                test_cases.append(test_case)

        except (OSError, ValueError) as e:
            print(f"Error processing {file_path}: {e}")

    return test_cases
