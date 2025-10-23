"""Sequence reference registry.

Maps refget accessions (``SQ.*``) to a tuple of (:class:`Assembly`, :class:`Chromosome`)
and exposes helpers to look up the assembly/chromosome for a given ID. The registry is
curated for internally-used builds (currently ``hg19``/``hg38``); extend as needed.
"""

import logging
import re
from enum import StrEnum

_logger = logging.getLogger(__name__)


class Assembly(StrEnum):
    """Constrain reference genome assembly values.

    We could conceivably support every UCSC chainfile offering, but for now, we'll
    stick with internal use cases only.
    """

    HG38 = "hg38"
    HG19 = "hg19"


class Chromosome(StrEnum):
    """Constrain chromosome values to UCSC-style names.

    This class should NOT be used to type-constrain input in the converter
    module, because in practice, chainfiles can use any name for an accession. In practice,
    though, we're mostly interested in UCSC chainfiles, so this class is provided as a
    utility for likely-relevant chromosome names.
    """

    CHR1 = "chr1"
    CHR2 = "chr2"
    CHR3 = "chr3"
    CHR4 = "chr4"
    CHR5 = "chr5"
    CHR6 = "chr6"
    CHR7 = "chr7"
    CHR8 = "chr8"
    CHR9 = "chr9"
    CHR10 = "chr10"
    CHR11 = "chr11"
    CHR12 = "chr12"
    CHR13 = "chr13"
    CHR14 = "chr14"
    CHR15 = "chr15"
    CHR16 = "chr16"
    CHR17 = "chr17"
    CHR18 = "chr18"
    CHR19 = "chr19"
    CHR20 = "chr20"
    CHR21 = "chr21"
    CHR22 = "chr22"
    CHRX = "chrX"
    CHRY = "chrY"


REFGET_ID_INFO = {
    "SQ.Ya6Rs7DHhDeg7YaOSg1EoNi3U_nQ9SvO": (Assembly.HG38, Chromosome.CHR1),
    "SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g": (Assembly.HG38, Chromosome.CHR2),
    "SQ.Zu7h9AggXxhTaGVsy7h_EZSChSZGcmgX": (Assembly.HG38, Chromosome.CHR3),
    "SQ.HxuclGHh0XCDuF8x6yQrpHUBL7ZntAHc": (Assembly.HG38, Chromosome.CHR4),
    "SQ.aUiQCzCPZ2d0csHbMSbh2NzInhonSXwI": (Assembly.HG38, Chromosome.CHR5),
    "SQ.0iKlIQk2oZLoeOG9P1riRU6hvL5Ux8TV": (Assembly.HG38, Chromosome.CHR6),
    "SQ.F-LrLMe1SRpfUZHkQmvkVKFEGaoDeHul": (Assembly.HG38, Chromosome.CHR7),
    "SQ.209Z7zJ-mFypBEWLk4rNC6S_OxY5p7bs": (Assembly.HG38, Chromosome.CHR8),
    "SQ.KEO-4XBcm1cxeo_DIQ8_ofqGUkp4iZhI": (Assembly.HG38, Chromosome.CHR9),
    "SQ.ss8r_wB0-b9r44TQTMmVTI92884QvBiB": (Assembly.HG38, Chromosome.CHR10),
    "SQ.2NkFm8HK88MqeNkCgj78KidCAXgnsfV1": (Assembly.HG38, Chromosome.CHR11),
    "SQ.6wlJpONE3oNb4D69ULmEXhqyDZ4vwNfl": (Assembly.HG38, Chromosome.CHR12),
    "SQ._0wi-qoDrvram155UmcSC-zA5ZK4fpLT": (Assembly.HG38, Chromosome.CHR13),
    "SQ.eK4D2MosgK_ivBkgi6FVPg5UXs1bYESm": (Assembly.HG38, Chromosome.CHR14),
    "SQ.AsXvWL1-2i5U_buw6_niVIxD6zTbAuS6": (Assembly.HG38, Chromosome.CHR15),
    "SQ.yC_0RBj3fgBlvgyAuycbzdubtLxq-rE0": (Assembly.HG38, Chromosome.CHR16),
    "SQ.dLZ15tNO1Ur0IcGjwc3Sdi_0A6Yf4zm7": (Assembly.HG38, Chromosome.CHR17),
    "SQ.vWwFhJ5lQDMhh-czg06YtlWqu0lvFAZV": (Assembly.HG38, Chromosome.CHR18),
    "SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl": (Assembly.HG38, Chromosome.CHR19),
    "SQ.-A1QmD_MatoqxvgVxBLZTONHz9-c7nQo": (Assembly.HG38, Chromosome.CHR20),
    "SQ.5ZUqxCmDDgN4xTRbaSjN8LwgZironmB8": (Assembly.HG38, Chromosome.CHR21),
    "SQ.7B7SHsmchAR0dFcDCuSFjJAo7tX87krQ": (Assembly.HG38, Chromosome.CHR22),
    "SQ.w0WZEvgJF0zf_P4yyTzjjv9oW1z61HHP": (Assembly.HG38, Chromosome.CHRX),
    "SQ.8_liLu1aycC0tPQPFmUaGXJLDs5SbPZ5": (Assembly.HG38, Chromosome.CHRY),
    "SQ.S_KjnFVz-FE7M0W6yoaUDgYxLPc1jyWU": (Assembly.HG19, Chromosome.CHR1),
    "SQ.9KdcA9ZpY1Cpvxvg8bMSLYDUpsX6GDLO": (Assembly.HG19, Chromosome.CHR2),
    "SQ.VNBualIltAyi2AI_uXcKU7M9XUOuA7MS": (Assembly.HG19, Chromosome.CHR3),
    "SQ.iy7Zfceb5_VGtTQzJ-v5JpPbpeifHD_V": (Assembly.HG19, Chromosome.CHR4),
    "SQ.vbjOdMfHJvTjK_nqvFvpaSKhZillW0SX": (Assembly.HG19, Chromosome.CHR5),
    "SQ.KqaUhJMW3CDjhoVtBetdEKT1n6hM-7Ek": (Assembly.HG19, Chromosome.CHR6),
    "SQ.IW78mgV5Cqf6M24hy52hPjyyo5tCCd86": (Assembly.HG19, Chromosome.CHR7),
    "SQ.tTm7wmhz0G4lpt8wPspcNkAD_qiminj6": (Assembly.HG19, Chromosome.CHR8),
    "SQ.HBckYGQ4wYG9APHLpjoQ9UUe9v7NxExt": (Assembly.HG19, Chromosome.CHR9),
    "SQ.-BOZ8Esn8J88qDwNiSEwUr5425UXdiGX": (Assembly.HG19, Chromosome.CHR10),
    "SQ.XXi2_O1ly-CCOi3HP5TypAw7LtC6niFG": (Assembly.HG19, Chromosome.CHR11),
    "SQ.105bBysLoDFQHhajooTAUyUkNiZ8LJEH": (Assembly.HG19, Chromosome.CHR12),
    "SQ.Ewb9qlgTqN6e_XQiRVYpoUfZJHXeiUfH": (Assembly.HG19, Chromosome.CHR13),
    "SQ.5Ji6FGEKfejK1U6BMScqrdKJK8GqmIGf": (Assembly.HG19, Chromosome.CHR14),
    "SQ.zIMZb3Ft7RdWa5XYq0PxIlezLY2ccCgt": (Assembly.HG19, Chromosome.CHR15),
    "SQ.W6wLoIFOn4G7cjopxPxYNk2lcEqhLQFb": (Assembly.HG19, Chromosome.CHR16),
    "SQ.AjWXsI7AkTK35XW9pgd3UbjpC3MAevlz": (Assembly.HG19, Chromosome.CHR17),
    "SQ.BTj4BDaaHYoPhD3oY2GdwC_l0uqZ92UD": (Assembly.HG19, Chromosome.CHR18),
    "SQ.ItRDD47aMoioDCNW_occY5fWKZBKlxCX": (Assembly.HG19, Chromosome.CHR19),
    "SQ.iy_UbUrvECxFRX5LPTH_KPojdlT7BKsf": (Assembly.HG19, Chromosome.CHR20),
    "SQ.LpTaNW-hwuY_yARP0rtarCnpCQLkgVCg": (Assembly.HG19, Chromosome.CHR21),
    "SQ.XOgHwwR3Upfp5sZYk6ZKzvV25a4RBVu8": (Assembly.HG19, Chromosome.CHR22),
    "SQ.v7noePfnNpK8ghYXEqZ9NukMXW7YeNsm": (Assembly.HG19, Chromosome.CHRX),
    "SQ.BT7QyW5iXaX_1PSX-msSGYsqRdMKqkj-": (Assembly.HG19, Chromosome.CHRY),
}

REFGET_ID_LOOKUP = {v: k for k, v in REFGET_ID_INFO.items()}


_ERROR_PATTERN = re.compile(r"^SQ\.[0-9A-Za-z_\\-]{32}$")


def get_seqinfo_from_refget_id(
    refget_accession: str,
) -> tuple[Assembly, Chromosome] | None:
    """Given a GA4GH SequenceReference refget accession ID, get back its reference genome and chromosome name

    .. code-block:: pycon

        >>> from agct.assembly_registry import get_assembly_from_refget_id
        >>> get_assembly_from_refget_id("SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g")
        (<Assembly.HG38: 'hg38'>, <Chromosome.CHR2: 'chr2'>)

    Use for acquiring a converter instance and calling liftover on a referenced GA4GH
    variation object.

    :param refget_accession: sequence reference (must start with `"SQ."`)
    :return: a reference assembly and chromosome, if successful
    :raise ValueError: if input appears to be in an invalid format for a refget accession ID
    """
    if not re.match(_ERROR_PATTERN, refget_accession):
        msg = f"refget accession ID must be in format 'SQ.ABCDEFGHIJKLMNOPQRSTUVWXYZ123456'; got {refget_accession}"
        _logger.error(msg)
        raise ValueError(msg)
    return REFGET_ID_INFO.get(refget_accession)


def get_refget_id_from_seqinfo(
    assembly: Assembly, chromosome: Chromosome
) -> str | None:
    """Given an assembly/chromosome pairing, get a refget accession ID, if known

    :param assembly: reference assembly for sequence
    :param chromosome: chromosome name
    :return: a refget sequence accession ID, if known
    """
    return REFGET_ID_LOOKUP.get((assembly, chromosome))
