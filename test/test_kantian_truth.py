import pytest

from test._helpers import get_verdict
from test.ground_truth import KANTIAN_TRUTH


@pytest.mark.parametrize(
    "dilemma_name, expected", KANTIAN_TRUTH.items()
)
def test_kantian_verdict(dilemma_name, expected, evaluation):
    result = get_verdict(evaluation(dilemma_name), "kantian")

    assert result is expected, (
        f"{dilemma_name}: expected permissible={expected}, got {result}"
    )