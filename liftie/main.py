"""Perform chainfile-driven liftover."""
from enum import Enum

import liftie._liftie as _liftie


class Strand(str, Enum):

    SENSE = "+"
    ANTISENSE = "-"


class Liftie:
    """Liftover provider for a single DB to DB association."""

    def __init__(self, from_db: str, to_db: str) -> None:
        """Initialize liftover instance.

        :param from_db: database name, e.g. ``"hg19"``
        :param to_db: database name, e.g. ``"hg19"``
        """
        self._lifter = _liftie.Lifter(from_db, to_db)

    def liftover(self, chrom: str, pos: int, strand: Strand = Strand.SENSE) -> str:
        """Perform liftover for given params

        :param chrom: chromosome name as given in chainfile. Usually e.g. ``"chr7"``.
        :param pos: query position
        :param strand: query strand (``"+"`` by default)
        :return: first match TODO return whole list
        """
        return self._lifter.lift(chrom, pos)
