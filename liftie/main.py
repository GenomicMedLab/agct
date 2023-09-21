"""Perform chainfile-driven liftover."""
from enum import Enum

import liftie._liftie as _liftie


class Strand(str, Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class Liftie:
    """Liftover provider for a single DB to DB association."""

    def __init__(self, from_db: str, to_db: str) -> None:
        """Initialize liftover instance.

        :param from_db: database name, e.g. ``"19"``
        :param to_db: database name, e.g. ``"38"``
        """
        self._lifter = _liftie.Lifter(from_db, to_db)

    def convert_coordinate(
        self, chrom: str, pos: int, strand: Strand = Strand.POSITIVE
    ) -> str:
        """Perform liftover for given params

        The ``Strand`` enum provides helpful constraints for legal strand values:

        .. code-block:: python

           from liftie.main import Liftie, Strand

           lifter = Liftie("19", "38")
           lifter.convert_coordinate("chr7", 140453136, Strand.POSITIVE)
           # returns [['chr7', '140753336', '+']]


        :param chrom: chromosome name as given in chainfile. Usually e.g. ``"chr7"``.
        :param pos: query position
        :param strand: query strand (``"+"`` by default).
        :return: first match TODO return whole list
        """
        return self._lifter.lift(chrom, pos, strand)
