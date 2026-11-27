import json

import pytest

from ethico.validator import UnifiedModel
from test._helpers import case_files


@pytest.mark.parametrize("file_path", case_files(), ids=lambda path: path.parent.name)
def test_unified_model_validation(file_path):
    model_data = json.loads(file_path.read_text(encoding="utf-8"))
    UnifiedModel.model_validate(model_data)
