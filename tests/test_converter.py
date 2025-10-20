"""Module for testing Converter initialization"""

import re
from pathlib import Path

import pytest

from agct import Assembly, Converter


def test_valid(data_dir: Path):
    """Test valid initialization"""
    assert Converter(
        chainfile=str(data_dir / "ucsc-chainfile" / "chainfile_hg19_to_hg38_.chain")
    )


def test_invalid():
    """Test invalid initialization"""
    with pytest.raises(ValueError, match="Must provide both `from_db` and `to_db`"):
        Converter()

    with pytest.raises(
        ValueError, match=re.escape("Liftover must be to/from different sources.")
    ):
        Converter(Assembly.HG19, Assembly.HG19)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Unable to coerce to_db value 'hg18' to a known reference genome: [<Assembly.HG38: 'hg38'>, <Assembly.HG19: 'hg19'>]"
        ),
    ):
        Converter(Assembly.HG19, "hg18")
