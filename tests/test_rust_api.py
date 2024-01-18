"""Test some non-public aspects of the Rust layer."""
import pytest

from chainlifter._core import ChainfileError, ChainLifter


def test_open_chainfile_errors(data_dir):
    """Test chainfile opening/reading errors."""
    with pytest.raises(FileNotFoundError):
        ChainLifter(str(data_dir / "non_existent_chainfile.chain"))
    with pytest.raises(ChainfileError):
        ChainLifter(str(data_dir / "invalid_chainfile.chain"))
