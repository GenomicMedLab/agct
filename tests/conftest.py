"""Configure tests."""
import os
from pathlib import Path


def pytest_sessionstart(session):
    """Perform actions after Session object is created.

    * set test data directory
    """
    os.environ["WAGS_TAILS_DIR"] = str(Path(__file__).parents[0] / "data")
