"""Parcours récursif d'un projet (cf. ARCHITECTURE.md)."""

from pathlib import Path
from typing import List, NamedTuple, Optional

from pep8_scanner.core.analyzer import analyze_file
from pep8_scanner.rules.base import Violation

EXCLUDED_DIR_NAMES = {"__pycache__"}


class FileScanResult(NamedTuple):
    filepath: str
    violations: List[Violation]
    error: Optional[str]


def find_python_files(root_path) -> List[Path]:
    """Liste, de façon récursive, les fichiers .py d'un projet, en
    excluant les répertoires cachés (ex: .git, .venv) et __pycache__."""
    root = Path(root_path)

    def est_exclu(fichier: Path) -> bool:
        dossiers = fichier.relative_to(root).parts[:-1]
        return any(
            partie.startswith(".") or partie in EXCLUDED_DIR_NAMES
            for partie in dossiers
        )

    return sorted(
        fichier for fichier in root.rglob("*.py") if not est_exclu(fichier)
    )


def scan_project(root_path, profile: Optional[str] = None) -> List[FileScanResult]:
    """Analyse récursivement un dossier projet et retourne un résultat
    par fichier .py trouvé. Un fichier avec une erreur de syntaxe est
    signalé via le champ `error` plutôt que d'interrompre le scan."""
    root = Path(root_path)
    if not root.is_dir():
        raise NotADirectoryError(
            "'{}' n'est pas un dossier valide.".format(root_path)
        )

    results = []
    for filepath in find_python_files(root):
        try:
            violations = analyze_file(filepath, profile=profile)
        except SyntaxError as exc:
            results.append(
                FileScanResult(filepath=str(filepath), violations=[], error=str(exc))
            )
        else:
            results.append(
                FileScanResult(filepath=str(filepath), violations=violations, error=None)
            )
    return results
