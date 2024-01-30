"""Test some non-public aspects of the Rust layer."""
import pytest

from agct._core import ChainfileError, Converter


def test_open_chainfile_errors(data_dir):
    """Test chainfile opening/reading errors."""
    with pytest.raises(FileNotFoundError):
        Converter(str(data_dir / "non_existent_chainfile.chain"))
    with pytest.raises(ChainfileError):
        Converter(str(data_dir / "invalid_chainfile.chain"))
