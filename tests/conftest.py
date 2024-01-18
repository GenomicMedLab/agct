"""Configure tests."""
import os
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parents[0] / "data"


def pytest_sessionstart(session):
    """Perform actions after Session object is created.

    * set test data directory
    """
    os.environ["WAGS_TAILS_DIR"] = str(DATA_DIR)


@pytest.fixture(scope="module")
def data_dir():
    """Provide test data directory as a fixture."""
    return DATA_DIR
