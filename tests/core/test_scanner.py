from pathlib import Path

import pytest

# Déclenche l'enregistrement des règles dans le registre global, pour que
# ce module de test soit indépendant de l'ordre de collecte de pytest.
import pep8_scanner.rules.pep8.line_length  # noqa: F401
import pep8_scanner.rules.pep8.whitespace  # noqa: F401
from pep8_scanner.core.config import ScanConfig
from pep8_scanner.core.scanner import find_python_files, scan_project
from pep8_scanner.rules.base import Severity


def resultats_par_nom(resultats):
    return {Path(r.filepath).name: r for r in resultats}


def test_find_python_files_trouve_les_fichiers_py_recursivement(tmp_path):
    (tmp_path / "module.py").write_text("x = 1\n")
    sous_dossier = tmp_path / "paquet"
    sous_dossier.mkdir()
    (sous_dossier / "sous_module.py").write_text("y = 2\n")
    (tmp_path / "notes.txt").write_text("pas du python\n")

    fichiers = find_python_files(tmp_path)

    noms = {f.name for f in fichiers}
    assert noms == {"module.py", "sous_module.py"}


def test_find_python_files_exclut_dossiers_caches_et_pycache(tmp_path):
    (tmp_path / "module.py").write_text("x = 1\n")

    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "ignore_moi.py").write_text("z = 3\n")

    pycache = tmp_path / "__pycache__"
    pycache.mkdir()
    (pycache / "ignore_moi_aussi.py").write_text("z = 3\n")

    fichiers = find_python_files(tmp_path)

    assert {f.name for f in fichiers} == {"module.py"}


def test_scan_project_agrege_les_violations_de_plusieurs_fichiers(tmp_path):
    (tmp_path / "propre.py").write_text("x = 1\n")
    (tmp_path / "sale.py").write_text("x = 1   \n")

    resultats = resultats_par_nom(scan_project(tmp_path, profile="pep8"))

    assert resultats["propre.py"].violations == []
    assert resultats["propre.py"].error is None
    assert any(v.rule_code == "W291" for v in resultats["sale.py"].violations)
    assert resultats["sale.py"].error is None


def test_scan_project_signale_une_erreur_de_syntaxe_sans_planter(tmp_path):
    (tmp_path / "casse.py").write_text("def incomplet(\n")
    (tmp_path / "propre.py").write_text("x = 1\n")

    resultats = resultats_par_nom(scan_project(tmp_path, profile="pep8"))

    assert resultats["casse.py"].error is not None
    assert resultats["casse.py"].violations == []
    assert resultats["casse.py"].loc == 0
    assert resultats["propre.py"].error is None


def test_scan_project_expose_le_loc_par_fichier(tmp_path):
    (tmp_path / "trois_lignes.py").write_text("x = 1\ny = 2\nz = 3\n")

    resultats = resultats_par_nom(scan_project(tmp_path, profile="pep8"))

    assert resultats["trois_lignes.py"].loc == 3


def test_scan_project_leve_une_erreur_si_le_dossier_nexiste_pas(tmp_path):
    inexistant = tmp_path / "nexiste_pas"

    with pytest.raises(NotADirectoryError):
        scan_project(inexistant)


def test_scan_project_applique_la_config_ignored_rules(tmp_path):
    (tmp_path / "sale.py").write_text("x = 1   \n")
    config = ScanConfig(ignored_rules=frozenset({"W291"}), severity_overrides={})

    resultats = resultats_par_nom(scan_project(tmp_path, profile="pep8", config=config))

    assert resultats["sale.py"].violations == []


def test_scan_project_applique_la_config_severity_overrides(tmp_path):
    (tmp_path / "sale.py").write_text("x = 1   \n")
    config = ScanConfig(
        ignored_rules=frozenset(), severity_overrides={"W291": Severity.CRITIQUE}
    )

    resultats = resultats_par_nom(scan_project(tmp_path, profile="pep8", config=config))

    w291 = next(v for v in resultats["sale.py"].violations if v.rule_code == "W291")
    assert w291.severity == Severity.CRITIQUE
