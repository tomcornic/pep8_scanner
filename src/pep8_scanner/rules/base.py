"""Interface commune des règles (cf. ARCHITECTURE.md et NOTATION.md)."""

from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List, NamedTuple


class Severity(IntEnum):
    """Paliers de gravité et poids associés (cf. NOTATION.md)."""

    MINEUR = 1
    MODERE = 2
    MAJEUR = 4
    CRITIQUE = 8


class Violation(NamedTuple):
    rule_code: str
    line: int
    column: int
    message: str
    severity: Severity


class BaseRule(ABC):
    """Toute règle (PEP 8, PEP 257, ou norme future) doit hériter de
    cette classe et renseigner ses attributs de description.
    """

    code = None
    name = None
    description = None
    severity = None
    category = None

    @abstractmethod
    def check(self, context) -> List[Violation]:
        """Analyse le contexte fourni et retourne la liste des
        infractions détectées pour cette règle."""
        raise NotImplementedError
