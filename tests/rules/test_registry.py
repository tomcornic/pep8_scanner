import pytest

from pep8_scanner.rules.base import BaseRule, Severity
from pep8_scanner.rules.registry import RuleRegistry


class RegleFactice(BaseRule):
    code = "X001"
    name = "regle_factice"
    description = "Règle de test"
    severity = Severity.MINEUR
    category = "test"

    def check(self, context):
        return []


class AutreRegleFactice(BaseRule):
    code = "X002"
    name = "autre_regle_factice"
    description = "Autre règle de test"
    severity = Severity.MAJEUR
    category = "test"

    def check(self, context):
        return []


def test_register_adds_rule_to_registry_and_profile():
    registry = RuleRegistry()

    registry.register(profile="pep8")(RegleFactice)

    assert registry.get_rule("X001") is RegleFactice
    assert registry.get_rules(profile="pep8") == [RegleFactice]


def test_get_rules_without_profile_returns_all_registered_rules():
    registry = RuleRegistry()
    registry.register(profile="pep8")(RegleFactice)
    registry.register(profile="pep257")(AutreRegleFactice)

    assert set(registry.get_rules()) == {RegleFactice, AutreRegleFactice}


def test_get_rules_for_unknown_profile_returns_empty_list():
    registry = RuleRegistry()

    assert registry.get_rules(profile="inconnu") == []


def test_profiles_lists_registered_profile_names():
    registry = RuleRegistry()
    registry.register(profile="pep8")(RegleFactice)
    registry.register(profile="pep257")(AutreRegleFactice)

    assert set(registry.profiles()) == {"pep8", "pep257"}


def test_register_rule_without_code_raises():
    registry = RuleRegistry()

    class RegleSansCode(BaseRule):
        code = None

        def check(self, context):
            return []

    with pytest.raises(ValueError):
        registry.register(profile="pep8")(RegleSansCode)


def test_register_duplicate_code_raises():
    registry = RuleRegistry()
    registry.register(profile="pep8")(RegleFactice)

    class RegleDupliquee(BaseRule):
        code = "X001"

        def check(self, context):
            return []

    with pytest.raises(ValueError):
        registry.register(profile="pep8")(RegleDupliquee)
