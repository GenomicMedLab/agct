"""Run liftover tests."""

from agct import Assembly, Converter, Strand


def test_hg19_to_hg38():
    """Test hg19 to hg38 lifter."""
    converter = Converter(Assembly.HG19, Assembly.HG38)

    result = converter.convert_coordinate("chr7", 140439611)
    assert len(result) == 1
    assert result[0] == ("chr7", 140739811, Strand.POSITIVE)

    result = converter.convert_coordinate("chr7", 140439746)
    assert len(result) == 1
    assert result[0] == ("chr7", 140739946, Strand.POSITIVE)

    result = converter.convert_coordinate("chr7", 140439703)
    assert len(result) == 1
    assert result[0] == ("chr7", 140739903, Strand.POSITIVE)

    result = converter.convert_coordinate("chr7", 140453136)
    assert len(result) == 1
    assert result[0] == ("chr7", 140753336, Strand.POSITIVE)

    result = converter.convert_coordinate("chr1", 206072707)
    assert len(result) == 1
    assert result[0] == ("chr1", 206268644, Strand.NEGATIVE)

    # coordinate exceeds bounds
    result = converter.convert_coordinate("chr7", 14040053136)
    assert result == []


def test_hg38_to_hg19():
    """Test hg38 to hg19 lifter."""
    converter = Converter(Assembly.HG38, Assembly.HG19)

    result = converter.convert_coordinate("chr7", 140739811)
    assert len(result) == 1
    assert result[0] == ("chr7", 140439611, Strand.POSITIVE)

    result = converter.convert_coordinate("chr7", 140759820)
    assert len(result) == 1
    assert result[0] == ("chr7", 140459620, Strand.POSITIVE)

    result = converter.convert_coordinate("chr7", 60878240)
    assert len(result) == 1
    assert result[0] == ("chr7", 61646115, Strand.POSITIVE)
