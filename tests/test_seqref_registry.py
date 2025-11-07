import pytest

from agct.seqref_registry import (
    Assembly,
    Chromosome,
    get_refget_id_from_seqinfo,
    get_seqinfo_from_refget_id,
)


def test_assembly_enum():
    assert Assembly("hg38") == Assembly.HG38
    assert Assembly.HG38 == "hg38"
    assert Assembly("hg19") == Assembly.HG19
    assert Assembly.HG19 == "hg19"


def test_assembly_enum_to_ncbi():
    assert Assembly.HG19.as_grc == "GRCh37"
    assert Assembly.HG38.as_grc == "GRCh38"


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


def test_seqid_fetcher():
    assert (
        get_refget_id_from_seqinfo(
            Assembly.HG38,
            Chromosome.CHR10,
        )
        == "SQ.ss8r_wB0-b9r44TQTMmVTI92884QvBiB"
    )
    assert (
        get_refget_id_from_seqinfo(
            Assembly.HG19,
            Chromosome.CHR10,
        )
        == "SQ.-BOZ8Esn8J88qDwNiSEwUr5425UXdiGX"
    )
    assert (
        get_refget_id_from_seqinfo(
            Assembly.HG38,
            Chromosome.CHR6,
        )
        == "SQ.0iKlIQk2oZLoeOG9P1riRU6hvL5Ux8TV"
    )
    assert (
        get_refget_id_from_seqinfo(
            Assembly.HG19,
            Chromosome.CHR6,
        )
        == "SQ.KqaUhJMW3CDjhoVtBetdEKT1n6hM-7Ek"
    )
    assert (
        get_refget_id_from_seqinfo(
            Assembly.HG19,
            Chromosome.CHR21,
        )
        == "SQ.LpTaNW-hwuY_yARP0rtarCnpCQLkgVCg"
    )
    assert (
        get_refget_id_from_seqinfo(
            Assembly.HG19,
            Chromosome.CHRX,
        )
        == "SQ.v7noePfnNpK8ghYXEqZ9NukMXW7YeNsm"
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
