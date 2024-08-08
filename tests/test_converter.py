"""Module for testing Converter initialization"""

import re

import pytest
from tests.conftest import DATA_DIR

from agct import Converter, Genome


def test_valid():
    """Test valid initialization"""
    assert Converter(
        chainfile=str(DATA_DIR / "ucsc-chainfile" / "chainfile_hg19_to_hg38_.chain")
    )


def test_invalid():
    """Test invalid initialization"""
    with pytest.raises(ValueError, match="Must provide both `from_db` and `to_db`"):
        Converter()

    with pytest.raises(ValueError, match="Liftover must be to/from different sources."):
        Converter(Genome.HG19, Genome.HG19)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Unable to coerce to_db value 'hg18' to a known reference genome: [<Genome.HG38: 'hg38'>, <Genome.HG19: 'hg19'>]"
        ),
    ):
        Converter(Genome.HG19, "hg18")
