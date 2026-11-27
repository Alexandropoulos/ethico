import pytest

from test._helpers import run_evaluation


@pytest.fixture
def evaluation(tmp_path):
    def evaluate(dilemma_name):
        return run_evaluation(dilemma_name, tmp_path)

    return evaluate
