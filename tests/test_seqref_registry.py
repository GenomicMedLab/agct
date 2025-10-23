import pytest

from agct.seqref_registry import Assembly, Chromosome, get_seqinfo_from_refget_id


def test_assembly_fetcher():
    assert get_seqinfo_from_refget_id("SQ.ss8r_wB0-b9r44TQTMmVTI92884QvBiB") == (
        Assembly.HG38,
        Chromosome.CHR10,
    )
    assert get_seqinfo_from_refget_id("SQ.-BOZ8Esn8J88qDwNiSEwUr5425UXdiGX") == (
        Assembly.HG19,
        Chromosome.CHR10,
    )
    assert get_seqinfo_from_refget_id("SQ.0iKlIQk2oZLoeOG9P1riRU6hvL5Ux8TV") == (
        Assembly.HG38,
        Chromosome.CHR6,
    )
    assert get_seqinfo_from_refget_id("SQ.KqaUhJMW3CDjhoVtBetdEKT1n6hM-7Ek") == (
        Assembly.HG19,
        Chromosome.CHR6,
    )
    assert get_seqinfo_from_refget_id("SQ.LpTaNW-hwuY_yARP0rtarCnpCQLkgVCg") == (
        Assembly.HG19,
        Chromosome.CHR21,
    )
    assert get_seqinfo_from_refget_id("SQ.v7noePfnNpK8ghYXEqZ9NukMXW7YeNsm") == (
        Assembly.HG19,
        Chromosome.CHRX,
    )


def test_unknown_sequences():
    assert get_seqinfo_from_refget_id("SQ.KqX7SGMq4GLY21TCAHPMWfNy-cFdT44h") is None


def test_invalid_input():
    input_string = "ga4gh:SQ.KqaUhJMW3CDjhoVtBetdEKT1n6hM-7Ek"
    with pytest.raises(
        ValueError,
        match=f"refget accession ID must be in format 'SQ.ABCDEFGHIJKLMNOPQRSTUVWXYZ123456'; got {input_string}",
    ):
        get_seqinfo_from_refget_id(input_string)
