"""Perform chainfile-driven liftover."""
from enum import Enum

import chainlifter._core as _core


class Strand(str, Enum):
    """Constrain strand values."""

    POSITIVE = "+"
    NEGATIVE = "-"


class ChainLifter:
    """Chainfile-based liftover provider for a single sequence to sequence
    association.
    """

    def __init__(self, from_db: str, to_db: str) -> None:
        """Initialize liftover instance.

        :param from_db: database name, e.g. ``"19"``
        :param to_db: database name, e.g. ``"38"``
        """
        self._chainlifter = _core.ChainLifter(from_db, to_db)

    def convert_coordinate(
        self, chrom: str, pos: int, strand: Strand = Strand.POSITIVE
    ) -> str:
        """Perform liftover for given params

        The ``Strand`` enum provides constraints for legal strand values:

        .. code-block:: python

           from chainlifter.lifter import ChainLifter, Strand

           lifter = ChainLifter("19", "38")
           lifter.convert_coordinate("chr7", 140453136, Strand.POSITIVE)
           # returns [['chr7', '140753336', '+']]


        :param chrom: chromosome name as given in chainfile. Usually e.g. ``"chr7"``.
        :param pos: query position
        :param strand: query strand (``"+"`` by default).
        :return: first match TODO return whole list
        """
        return self._chainlifter.lift(chrom, pos, strand)
