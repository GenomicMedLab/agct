"""Assembly registry.

This module maintains a curated mapping from GA4GH VRS `SequenceReference`
refget accession identifiers (the ``"SQ."`` IDs) to human reference assemblies
and exposes a helper to look up the assembly for a given ID. Assemblies are
represented by the :class:`Assembly` enum (UCSC-style labels: ``hg19``, ``hg38``).

Use :func:`get_assembly_from_refget_id` when you have a refget accession ID and
need to determine which assembly it belongs to. The mapping is intentionally
conservative and currently reflects internal use cases; extend it as needed.
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


ID_TO_REFERENCE_MAP = {
    Assembly.HG38: [
        # chr1
        "SQ.Ya6Rs7DHhDeg7YaOSg1EoNi3U_nQ9SvO",
        # chr2
        "SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g",
        # chr3
        "SQ.Zu7h9AggXxhTaGVsy7h_EZSChSZGcmgX",
        # chr4
        "SQ.HxuclGHh0XCDuF8x6yQrpHUBL7ZntAHc",
        # chr5
        "SQ.aUiQCzCPZ2d0csHbMSbh2NzInhonSXwI",
        # chr6
        "SQ.0iKlIQk2oZLoeOG9P1riRU6hvL5Ux8TV",
        # chr7
        "SQ.F-LrLMe1SRpfUZHkQmvkVKFEGaoDeHul",
        # chr8
        "SQ.209Z7zJ-mFypBEWLk4rNC6S_OxY5p7bs",
        # chr9
        "SQ.KEO-4XBcm1cxeo_DIQ8_ofqGUkp4iZhI",
        # chr10
        "SQ.ss8r_wB0-b9r44TQTMmVTI92884QvBiB",
        # chr11
        "SQ.2NkFm8HK88MqeNkCgj78KidCAXgnsfV1",
        # chr12
        "SQ.6wlJpONE3oNb4D69ULmEXhqyDZ4vwNfl",
        # chr13
        "SQ._0wi-qoDrvram155UmcSC-zA5ZK4fpLT",
        # chr14
        "SQ.eK4D2MosgK_ivBkgi6FVPg5UXs1bYESm",
        # chr15
        "SQ.AsXvWL1-2i5U_buw6_niVIxD6zTbAuS6",
        # chr16
        "SQ.yC_0RBj3fgBlvgyAuycbzdubtLxq-rE0",
        # chr17
        "SQ.dLZ15tNO1Ur0IcGjwc3Sdi_0A6Yf4zm7",
        # chr18
        "SQ.vWwFhJ5lQDMhh-czg06YtlWqu0lvFAZV",
        # chr19
        "SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
        # chr20
        "SQ.-A1QmD_MatoqxvgVxBLZTONHz9-c7nQo",
        # chr21
        "SQ.5ZUqxCmDDgN4xTRbaSjN8LwgZironmB8",
        # chr22
        "SQ.7B7SHsmchAR0dFcDCuSFjJAo7tX87krQ",
        # chr23
        "SQ.w0WZEvgJF0zf_P4yyTzjjv9oW1z61HHP",
        # chr24/chrY
        "SQ.8_liLu1aycC0tPQPFmUaGXJLDs5SbPZ5",
    ],
    Assembly.HG19: [
        # chr1
        "SQ.S_KjnFVz-FE7M0W6yoaUDgYxLPc1jyWU",
        # chr2
        "SQ.9KdcA9ZpY1Cpvxvg8bMSLYDUpsX6GDLO",
        # chr3
        "SQ.VNBualIltAyi2AI_uXcKU7M9XUOuA7MS",
        # chr4
        "SQ.iy7Zfceb5_VGtTQzJ-v5JpPbpeifHD_V",
        # chr5
        "SQ.vbjOdMfHJvTjK_nqvFvpaSKhZillW0SX",
        # chr6
        "SQ.KqaUhJMW3CDjhoVtBetdEKT1n6hM-7Ek",
        # chr7
        "SQ.IW78mgV5Cqf6M24hy52hPjyyo5tCCd86",
        # chr8
        "SQ.tTm7wmhz0G4lpt8wPspcNkAD_qiminj6",
        # chr9
        "SQ.HBckYGQ4wYG9APHLpjoQ9UUe9v7NxExt",
        # chr10
        "SQ.-BOZ8Esn8J88qDwNiSEwUr5425UXdiGX",
        # chr11
        "SQ.XXi2_O1ly-CCOi3HP5TypAw7LtC6niFG",
        # chr12
        "SQ.105bBysLoDFQHhajooTAUyUkNiZ8LJEH",
        # chr13
        "SQ.Ewb9qlgTqN6e_XQiRVYpoUfZJHXeiUfH",
        # chr14
        "SQ.5Ji6FGEKfejK1U6BMScqrdKJK8GqmIGf",
        # chr15
        "SQ.zIMZb3Ft7RdWa5XYq0PxIlezLY2ccCgt",
        # chr16
        "SQ.W6wLoIFOn4G7cjopxPxYNk2lcEqhLQFb",
        # chr17
        "SQ.AjWXsI7AkTK35XW9pgd3UbjpC3MAevlz",
        # chr18
        "SQ.BTj4BDaaHYoPhD3oY2GdwC_l0uqZ92UD",
        # chr19
        "SQ.ItRDD47aMoioDCNW_occY5fWKZBKlxCX",
        # chr20
        "SQ.iy_UbUrvECxFRX5LPTH_KPojdlT7BKsf",
        # chr21
        "SQ.LpTaNW-hwuY_yARP0rtarCnpCQLkgVCg",
        # chr22
        "SQ.XOgHwwR3Upfp5sZYk6ZKzvV25a4RBVu8",
        # chr23
        "SQ.v7noePfnNpK8ghYXEqZ9NukMXW7YeNsm",
        # chr24/chrY
        "SQ.BT7QyW5iXaX_1PSX-msSGYsqRdMKqkj-",
    ],
}


_error_pattern = re.compile(r"^SQ.[0-9A-Za-z_\\-]{32}$")


def get_assembly_from_refget_id(refget_accession: str) -> Assembly | None:
    """Given a GA4GH SequenceReference refget accession ID, get back its corresponding reference genome

    .. code-block:: pycon

        >>> from agct.assembly_registry import get_assembly_from_refget_id
        >>> get_assembly_from_refget_id("SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g")
        Genome.HG38

    Use to get an appropriate converter from a referenced GA4GH variation object.

    :param refget_accession: sequence reference (must start with `"SQ."`)
    :return: a reference assembly if recognized
    :raise ValueError: if input appears to be in an invalid format for a refget accession ID
    """
    for reference_genome, chromosome_accession_ids in ID_TO_REFERENCE_MAP.items():
        if refget_accession in chromosome_accession_ids:
            return reference_genome
    if not re.match(_error_pattern, refget_accession):
        msg = f"refget accession ID must be in format 'SQ.ABCDEFGHIJKLMNOPQRSTUVWXYZ123456'; got {refget_accession}"
        _logger.error(msg)
        raise ValueError(msg)
    return None
