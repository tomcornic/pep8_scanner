"""Calcul du score et de la note A-Z (cf. NOTATION.md)."""

from typing import Iterable, List, Tuple

from pep8_scanner.core.scanner import FileScanResult
from pep8_scanner.rules.base import Violation

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTER_INTERVAL_WIDTH = 2
# Dernière lettre finie (Y) commence à (26 - 1) * 2 = 50 exclu ; au-delà, Z.
MAX_FINITE_DENSITY = (len(LETTERS) - 1) * LETTER_INTERVAL_WIDTH


def compute_weighted_density(violations: Iterable[Violation], loc: int) -> float:
    """Densité pondérée = somme des poids des infractions / (LOC / 100)
    (cf. NOTATION.md). Un fichier sans lignes a une densité nulle."""
    if loc <= 0:
        return 0.0
    poids_total = sum(v.severity for v in violations)
    return poids_total / (loc / 100)


def grade_from_density(density: float) -> str:
    """Convertit une densité pondérée en lettre A-Z, par paliers réguliers
    de largeur 2 (cf. NOTATION.md)."""
    if density >= MAX_FINITE_DENSITY:
        return "Z"
    index = int(density // LETTER_INTERVAL_WIDTH)
    return LETTERS[index]


def grade_file(violations: Iterable[Violation], loc: int) -> str:
    return grade_from_density(compute_weighted_density(violations, loc))


def grade_project(file_reports: Iterable[Tuple[List[Violation], int]]) -> str:
    """Note globale d'un projet multi-fichiers : densité pondérée calculée
    sur l'ensemble des infractions et lignes de code du projet.
    Mathématiquement équivalent à la moyenne des densités par fichier
    pondérée par LOC (cf. NOTATION.md)."""
    toutes_violations: List[Violation] = []
    loc_total = 0
    for violations, loc in file_reports:
        toutes_violations.extend(violations)
        loc_total += loc
    return grade_file(toutes_violations, loc_total)


def grade_scan(results: Iterable[FileScanResult]) -> str:
    """Note globale à partir des résultats de `scan_project()`. Les
    fichiers en erreur de syntaxe sont exclus du calcul (pas de LOC
    fiable pour eux)."""
    return grade_project(
        (r.violations, r.loc) for r in results if r.error is None
    )
