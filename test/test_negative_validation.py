import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ethico.validator import (
    KantianModel,
    UnifiedModel,
    UtilitarianModel,
)

INVALID_CASES_DIR = Path(__file__).resolve().parents[1] / "data" / "invalid_test_cases"

ALL_MODELS = [KantianModel, UtilitarianModel, UnifiedModel]
KANTIAN_MODELS = [KantianModel, UnifiedModel]
UTILITARIAN_MODELS = [UtilitarianModel, UnifiedModel]


INVALID_CASES = [
    ("01_wrong_action_count", "actions", ALL_MODELS),
    ("02_missing_refrain", "actions", ALL_MODELS),
    ("03_empty_consequences", "consequences", ALL_MODELS),
    ("04_invalid_mechanism_key", "mechanisms", ALL_MODELS),
    ("05_missing_mechanism", "mechanisms", ALL_MODELS),
    ("06_empty_patients", "patients", KANTIAN_MODELS),
    ("07_invalid_affect_event", "affects", KANTIAN_MODELS),
    ("08_invalid_affect_valence", "affects", KANTIAN_MODELS),
    ("09_invalid_utility_key", "utilities", UTILITARIAN_MODELS),
    ("10_missing_utility", "utilities", UTILITARIAN_MODELS),
]


TEST_CASES = [
    pytest.param(
        dilemma_name,
        expected_field,
        model,
        id=f"{dilemma_name}-{model.__name__}",
    )
    for dilemma_name, expected_field, models in INVALID_CASES
    for model in models
]


@pytest.mark.parametrize(
    "dilemma_name, expected_field, model",
    TEST_CASES,
)
def test_invalid_model(dilemma_name, expected_field, model):
    situation_path = INVALID_CASES_DIR / dilemma_name / "situation.json"

    assert situation_path.is_file(), f"Missing test case: {situation_path}"

    with situation_path.open(encoding="utf-8") as f:
        model_data = json.load(f)

    with pytest.raises(ValidationError) as exc_info:
        model.model_validate(model_data)

    invalid_fields = {error["loc"][0] for error in exc_info.value.errors()}

    assert expected_field in invalid_fields, (
        f"Expected validation failure in '{expected_field}', "
        f"but got failures in {invalid_fields}"
    )
