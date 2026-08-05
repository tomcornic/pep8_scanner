import pytest

from pep8_scanner.rules.base import Severity, Violation
from pep8_scanner.scoring.grader import (
    compute_weighted_density,
    grade_file,
    grade_from_density,
    grade_project,
)


def violation(severity):
    return Violation(
        rule_code="X000", line=1, column=1, message="test", severity=severity
    )


def test_densite_nulle_sans_infraction():
    assert compute_weighted_density([], loc=100) == 0.0


def test_densite_respecte_la_formule_du_notation_md():
    violations = [violation(Severity.MAJEUR), violation(Severity.MAJEUR)]

    assert compute_weighted_density(violations, loc=100) == 8.0


def test_densite_est_nulle_si_pas_de_lignes():
    violations = [violation(Severity.CRITIQUE)]

    assert compute_weighted_density(violations, loc=0) == 0.0


@pytest.mark.parametrize(
    "density,lettre_attendue",
    [
        (0.0, "A"),
        (1.99, "A"),
        (2.0, "B"),
        (3.99, "B"),
        (48.0, "Y"),
        (49.99, "Y"),
        (50.0, "Z"),
        (100.0, "Z"),
    ],
)
def test_grade_from_density_respecte_la_table_du_notation_md(density, lettre_attendue):
    assert grade_from_density(density) == lettre_attendue


def test_grade_file_combine_densite_et_conversion():
    violations = [violation(Severity.MINEUR)]

    assert grade_file(violations, loc=100) == "A"


def test_grade_project_agrege_toutes_les_violations_et_loc():
    fichier_a = ([violation(Severity.CRITIQUE)], 50)
    fichier_b = ([violation(Severity.CRITIQUE)], 50)

    assert grade_project([fichier_a, fichier_b]) == grade_file(
        [violation(Severity.CRITIQUE), violation(Severity.CRITIQUE)], loc=100
    )


def test_grade_project_sans_fichier_retourne_a():
    assert grade_project([]) == "A"
