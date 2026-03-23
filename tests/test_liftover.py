"""Run liftover tests."""

import re

import pytest

from agct import Assembly, Converter, LiftoverResult, Strand


def test_hg19_to_hg38():
    """Test hg19 to hg38 lifter."""
    converter = Converter(Assembly.HG19, Assembly.HG38)

    result = converter.convert_coordinate("chr7", 140439611, 140439611)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 140739811, 140739811, Strand.POSITIVE, 14633688187
    )

    result = converter.convert_coordinate("chr7", 140439746, 140439746)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 140739946, 140739946, Strand.POSITIVE, 14633688187
    )

    result = converter.convert_coordinate("chr7", 140439703, 140439703)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 140739903, 140739903, Strand.POSITIVE, 14633688187
    )

    result = converter.convert_coordinate("chr7", 140453136, 140453136)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 140753336, 140753336, Strand.POSITIVE, 14633688187
    )

    result = converter.convert_coordinate("chr1", 206072707, 206072708)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr1", 206268644, 206268643, Strand.NEGATIVE, 24611930
    )


def test_hg38_to_hg19():
    """Test hg38 to hg19 lifter."""
    converter = Converter(Assembly.HG38, Assembly.HG19)

    result = converter.convert_coordinate("chr7", 140739811, 140739811)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 140439611, 140439611, Strand.POSITIVE, 14633759100
    )

    result = converter.convert_coordinate("chr7", 140759820, 140759820)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 140459620, 140459620, Strand.POSITIVE, 14633759100
    )

    result = converter.convert_coordinate("chr7", 60878240, 60878240)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 61646115, 61646115, Strand.POSITIVE, 2791030
    )

    result = converter.convert_coordinate("chr7", 60878240, 60878240)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 61646115, 61646115, Strand.POSITIVE, 2791030
    )

    result = converter.convert_coordinate("chr7", 60878240, 60878245)
    assert len(result) == 1
    assert result[0] == LiftoverResult(
        "chr7", 61646115, 61646120, Strand.POSITIVE, 2791030
    )


def test_interval_input():
    """Test that invalid intervals raise errors"""
    converter = Converter(Assembly.HG38, Assembly.HG19)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "`end` must be less than `start` on the positive strand: start=140739811, end=140739809"
        ),
    ):
        converter.convert_coordinate("chr7", 140739811, 140739809)

    with pytest.raises(
        ValueError,
        match=re.escape(
            "`start` must be less than `end` on the negative strand: start=206268644, end=206268645"
        ),
    ):
        converter.convert_coordinate(
            "chr1", 206268644, 206268645, strand=Strand.NEGATIVE
        )


def test_raises_for_int_overflow():
    converter = Converter(Assembly.HG19, Assembly.HG38)
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Coordinates exceed representable bounds of a 32 bit unsigned int: start=14040053136, end=14040053136 -- this is unsupported"
        ),
    ):
        converter.convert_coordinate("chr7", 14040053136, 14040053136)
