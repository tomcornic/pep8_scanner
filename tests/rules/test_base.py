import pytest

from pep8_scanner.rules.base import BaseRule, Severity, Violation


def test_severity_weights_match_notation_md():
    assert Severity.MINEUR == 1
    assert Severity.MODERE == 2
    assert Severity.MAJEUR == 4
    assert Severity.CRITIQUE == 8


def test_base_rule_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        BaseRule()


def test_violation_holds_expected_fields():
    violation = Violation(
        rule_code="E501",
        line=12,
        column=80,
        message="ligne trop longue",
        severity=Severity.MODERE,
    )

    assert violation.rule_code == "E501"
    assert violation.line == 12
    assert violation.column == 80
    assert violation.severity == Severity.MODERE


def test_concrete_rule_must_implement_check():
    class RegleSansCheck(BaseRule):
        code = "X000"

    with pytest.raises(TypeError):
        RegleSansCheck()


def test_concrete_rule_can_be_instantiated_and_checked():
    class RegleFactice(BaseRule):
        code = "X001"
        name = "regle_factice"
        description = "Règle de test"
        severity = Severity.MINEUR
        category = "test"

        def check(self, context):
            return []

    rule = RegleFactice()
    assert rule.check(context=None) == []
