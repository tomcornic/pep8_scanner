# Déclenche l'enregistrement des règles dans le registre global, pour que
# ce module de test soit indépendant de l'ordre de collecte de pytest.
import pep8_scanner.rules.pep8.blank_lines  # noqa: F401
import pep8_scanner.rules.pep8.line_length  # noqa: F401
import pep8_scanner.rules.pep8.whitespace  # noqa: F401
from pep8_scanner.report.explanations import (
    EXPLANATIONS,
    explain_violation,
    get_explanation,
)
from pep8_scanner.rules.base import Severity, Violation
from pep8_scanner.rules.registry import registry


def violation(rule_code, line=1, message="test"):
    return Violation(
        rule_code=rule_code,
        line=line,
        column=1,
        message=message,
        severity=Severity.MINEUR,
    )


def test_get_explanation_retourne_explication_pour_regle_connue():
    explanation = get_explanation("E501")

    assert explanation is not None
    assert "79 caractères" in explanation.why


def test_get_explanation_retourne_none_pour_regle_inconnue():
    assert get_explanation("X999") is None


def test_explain_violation_contient_le_code_et_la_ligne():
    texte = explain_violation(violation("W291", line=12))

    assert "W291" in texte
    assert "12" in texte


def test_explain_violation_se_rabat_sur_le_message_brut_si_regle_inconnue():
    texte = explain_violation(violation("X999", line=3, message="message brut"))

    assert "X999" in texte
    assert "message brut" in texte


def test_toutes_les_regles_enregistrees_du_profil_pep8_ont_une_explication():
    codes_enregistres = {r.code for r in registry.get_rules(profile="pep8")}

    codes_sans_explication = codes_enregistres - set(EXPLANATIONS.keys())

    assert codes_sans_explication == set()
