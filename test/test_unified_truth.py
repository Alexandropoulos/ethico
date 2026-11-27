import pytest

from test._helpers import get_verdict
from test.ground_truth import UNIFIED_TRUTH


@pytest.mark.parametrize(
    "dilemma_name, expected_kantian, expected_utilitarian",
    UNIFIED_TRUTH,
)
def test_theory_verdicts(
    dilemma_name,
    expected_kantian,
    expected_utilitarian,
    evaluation,
):
    result = evaluation(dilemma_name)

    actual_kantian = get_verdict(result, "kantian")
    actual_utilitarian = get_verdict(result, "utilitarian")

    assert actual_kantian is expected_kantian, (
        f"{dilemma_name} (Kantian): expected {expected_kantian}, got {actual_kantian}"
    )

    assert actual_utilitarian is expected_utilitarian, (
        f"{dilemma_name} (Utilitarian): "
        f"expected {expected_utilitarian}, got {actual_utilitarian}"
    )
