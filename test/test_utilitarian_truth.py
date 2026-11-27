import pytest

from test._helpers import get_verdict
from test.ground_truth import UTILITARIAN_TRUTH


@pytest.mark.parametrize("dilemma_name, expected", UTILITARIAN_TRUTH.items())
def test_utilitarian_verdict(dilemma_name, expected, evaluation):
    result = get_verdict(evaluation(dilemma_name), "utilitarian")

    assert result is expected, (
        f"{dilemma_name}: expected permissible={expected}, got {result}"
    )
