"""Run liftover tests."""
from chainlifter.lifter import ChainLifter, Genome, Strand


def test_hg19_to_hg38():
    """Test hg19 to hg38 lifter."""
    ch = ChainLifter(Genome.HG19, Genome.HG38)

    result = ch.convert_coordinate("chr7", 140439611)
    assert len(result) == 1
    assert result[0] == ("chr7", 140739811, Strand.POSITIVE)

    result = ch.convert_coordinate("chr7", 140439746)
    assert len(result) == 1
    assert result[0] == ("chr7", 140739946, Strand.POSITIVE)

    result = ch.convert_coordinate("chr7", 140439703)
    assert len(result) == 1
    assert result[0] == ("chr7", 140739903, Strand.POSITIVE)

    result = ch.convert_coordinate("chr7", 140453136)
    assert len(result) == 1
    assert result[0] == ("chr7", 140753336, Strand.POSITIVE)

    # coordinate exceeds bounds
    result = ch.convert_coordinate("chr7", 14040053136)
    assert result == []


def test_hg38_to_hg19():
    "Test hg38 to hg19 lifter." ""
    ch = ChainLifter(Genome.HG38, Genome.HG19)

    result = ch.convert_coordinate("chr7", 140739811)
    assert len(result) == 1
    assert result[0] == ("chr7", 140439611, Strand.POSITIVE)

    result = ch.convert_coordinate("chr7", 140759820)
    assert len(result) == 1
    assert result[0] == ("chr7", 140459620, Strand.POSITIVE)

    result = ch.convert_coordinate("chr7", 60878240)
    assert len(result) == 1
    assert result[0] == ("chr7", 61646115, Strand.POSITIVE)
