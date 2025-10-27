"""Module for testing Converter initialization"""

import re
from pathlib import Path

import pytest

from agct import Assembly, Converter, get_converter


def test_valid(data_dir: Path):
    """Test valid initialization"""
    assert Converter(
        chainfile=str(data_dir / "ucsc-chainfile" / "chainfile_hg19_to_hg38_.chain")
    )


def test_invalid():
    """Test invalid initialization"""
    with pytest.raises(
        ValueError, match="Must provide both `from_assembly` and `to_assembly`"
    ):
        Converter()

    with pytest.raises(
        ValueError, match=re.escape("Liftover must be to/from different sources.")
    ):
        Converter(Assembly.HG19, Assembly.HG19)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "Assembly args must be instance of `agct.seqref_registry.Genome`, instead got from_assembly=hg19 and to_assembly=hg18"
        ),
    ):
        Converter(Assembly.HG19, "hg18")


def test_factory_function():
    assert id(get_converter(Assembly.HG19, Assembly.HG38)) == id(
        get_converter(Assembly.HG19, Assembly.HG38)
    ), "Factory function isn't returning the same instance on successive calls"

    assert id(get_converter(Assembly.HG19, Assembly.HG38)) != id(
        get_converter(Assembly.HG38, Assembly.HG19)
    )
