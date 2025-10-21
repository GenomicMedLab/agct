"""Perform chainfile-driven liftover."""

import logging
from collections.abc import Callable
from enum import Enum
from pathlib import Path

from wags_tails import CustomData
from wags_tails.utils.downloads import download_http, handle_gzip
from wags_tails.utils.storage import get_data_dir

import agct._core as _core
from agct.assembly_registry import Assembly

_logger = logging.getLogger(__name__)


class Strand(str, Enum):
    """Constrain strand values."""

    POSITIVE = "+"
    NEGATIVE = "-"


class Converter:
    """Chainfile-based liftover provider for a single sequence to sequence
    association.
    """

    def __init__(
        self,
        from_assembly: Assembly | None = None,
        to_assembly: Assembly | None = None,
        chainfile: str | None = None,
    ) -> None:
        """Initialize liftover instance.

        Initialize with either ``from_assembly`` and ``to_assembly``, or directly with a chainfile.

        * If using assembly params, both must be provided, and they must be different
        * If using assembly params, the ``wags-tails`` library will be used to locate and, if
          necessary, acquire the pertinent chainfile from the UCSC web server. See
          the `wags-tails documentation <https://wags-tails.readthedocs.io/>`_ for more info.
        * If ``chainfile`` arg is provided, all other args are ignored.

        :param from_assembly: Assembly name, e.g. ``<Assembly.HG19>``
        :param to_assembly: database name, e.g. ``"hg38"``.
        :param chainfile: Path to chainfile
        :raise ValueError: if required arguments are not passed or are invalid
        :raise FileNotFoundError: if unable to open corresponding chainfile
        :raise _core.ChainfileError: if unable to read chainfile (i.e. it's invalid)
        """
        if not chainfile:
            if from_assembly is None or to_assembly is None:
                msg = "Must provide both `from_assembly` and `to_assembly`"
                raise ValueError(msg)

            if from_assembly == to_assembly:
                msg = "Liftover must be to/from different sources."
                raise ValueError(msg)

            data_handler = CustomData(
                f"chainfile_{from_assembly.value}_to_{to_assembly.value}",
                "chain",
                lambda: "",
                self._download_function_builder(from_assembly, to_assembly),
                data_dir=get_data_dir() / "ucsc-chainfile",
            )
            file, _ = data_handler.get_latest()
            chainfile = str(file.absolute())

        try:
            self._converter = _core.Converter(chainfile)
        except FileNotFoundError:
            _logger.exception("Unable to open chainfile located at %s", chainfile)
            raise
        except _core.ChainfileError:
            _logger.exception("Error reading chainfile located at %s", chainfile)
            raise

    @staticmethod
    def _download_function_builder(from_db: Assembly, to_db: Assembly) -> Callable:
        """Build downloader function for chainfile corresponding to source/destination
        params.

        Wags-Tails' custom data handler takes a downloader callback function. We
        construct it here, curried with from/to values in the download URL.

        :param from_db: genome lifting from
        :param to_db: genome lifting to
        :return: Function that downloads appropriate chainfile from UCSC
        """

        def _download_data(version: str, file: Path) -> None:  # noqa: ARG001
            """Download and gunzip chainfile from UCSC.

            :param version: not used
            :param file: path to save file to
            """
            url = f"https://hgdownload.soe.ucsc.edu/goldenPath/{from_db.value}/liftOver/{from_db.value}To{to_db.value.title()}.over.chain.gz"
            download_http(url, file, handler=handle_gzip)

        return _download_data

    def convert_coordinate(
        self, chrom: str, pos: int, strand: Strand = Strand.POSITIVE
    ) -> list[tuple[str, int, Strand]]:
        """Perform liftover for given params

        The ``Strand`` enum provides constraints for legal strand values:

        .. code-block:: python

           from agct import Converter, Strand, Assembly

           c = Converter(Assembly.HG19, Assembly.HG38)
           c.convert_coordinate("chr7", 140453136, Strand.POSITIVE)
           # returns [['chr7', 140753336, '+']]


        :param chrom: chromosome name as given in chainfile. Usually e.g. ``"chr7"``.
        :param pos: query position
        :param strand: query strand (``"+"`` by default).
        :return: list of coordinate matches (possibly empty)
        """
        try:
            results = self._converter.lift(chrom, pos, strand)
        except _core.NoLiftoverError:
            results = []
        except _core.ChainfileError:
            _logger.exception(
                "Encountered internal error while converting coordinates - is the chainfile invalid? (%s, %s, %s)",
                chrom,
                pos,
                strand,
            )
            results = []
        formatted_results: list[tuple[str, int, Strand]] = []
        for result in results:
            try:
                pos = int(result[1])
            except ValueError:
                _logger.exception("Got invalid position value in %s", result)
                continue
            try:
                strand = Strand(result[2])
            except ValueError:
                _logger.exception("Got invalid Strand value in %s", result)
                continue
            formatted_results.append((result[0], pos, strand))
        return formatted_results
