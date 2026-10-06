import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest
from django.test import override_settings

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def temp_data_dir(tmp_path: Path) -> Iterator[Path]:
    """Тесты работают с копией data/, а не с настоящими файлами."""
    data_dir = tmp_path / "data"
    shutil.copytree(ROOT / "data", data_dir)
    with override_settings(DATA_DIR=data_dir):
        yield data_dir
