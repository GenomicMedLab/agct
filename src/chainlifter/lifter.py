"""Perform chainfile-driven liftover."""
from enum import Enum, StrEnum
from pathlib import Path
from typing import Callable

from wags_tails import CustomData
from wags_tails.utils.downloads import download_http, handle_gzip
from wags_tails.utils.storage import get_data_dir

import chainlifter._core as _core


class Strand(StrEnum):
    """Constrain strand values."""

    POSITIVE = "+"
    NEGATIVE = "-"


class Genome(StrEnum):
    """Constrain genome values.

    We could conceivably support every UCSC chainfile offering, but for now, we'll
    stick with internal use cases only.
    """

    HG38 = "hg38"
    HG19 = "hg19"


class ChainLifter:
    """Chainfile-based liftover provider for a single sequence to sequence
    association.
    """

    def __init__(self, from_db: Genome, to_db: Genome) -> None:
        """Initialize liftover instance.

        :param from_db: database name, e.g. ``"19"``
        :param to_db: database name, e.g. ``"38"``
        """
        if from_db == to_db:
            raise ValueError("Liftover must be to/from different sources.")
        data_handler = CustomData(
            f"chainfile_{from_db.value}_to_{to_db.value}",
            "chain",
            lambda: "",
            self._download_function_builder(from_db, to_db),
            data_dir=get_data_dir() / "ucsc-chainfile",
        )
        file, _ = data_handler.get_latest()
        self._chainlifter = _core.ChainLifter(str(file.absolute()))

    @staticmethod
    def _download_function_builder(from_db: Genome, to_db: Genome) -> Callable:
        """Build downloader function for chainfile corresponding to source/destination
        params.

        Wags-Tails' custom data handler takes a downloader callback function. We
        construct it here, curried with from/to values in the download URL.

        :param from_db: genome lifting from
        :param to_db: genome lifting to
        :return: Function that downloads appropriate chainfile from UCSC
        """

        def _download_data(version: str, file: Path) -> None:
            """Download and gunzip chainfile from UCSC.

            :param version: not used
            :param file: path to save file to
            """
            url = f"https://hgdownload.soe.ucsc.edu/goldenPath/{from_db.value}/liftOver/{from_db.value}To{to_db.value.title()}.over.chain.gz"
            download_http(url, file, handler=handle_gzip)

        return _download_data

    def convert_coordinate(
        self, chrom: str, pos: int, strand: Strand = Strand.POSITIVE
    ) -> str:
        """Perform liftover for given params

        The ``Strand`` enum provides constraints for legal strand values:

        .. code-block:: python

           from chainlifter.lifter import ChainLifter, Strand

           lifter = ChainLifter("hg19", "hg38")
           lifter.convert_coordinate("chr7", 140453136, Strand.POSITIVE)
           # returns [['chr7', '140753336', '+']]


        :param chrom: chromosome name as given in chainfile. Usually e.g. ``"chr7"``.
        :param pos: query position
        :param strand: query strand (``"+"`` by default).
        :return: first match TODO return whole list
        """
        return self._chainlifter.lift(chrom, pos, strand)
