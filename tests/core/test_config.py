import json
from pathlib import Path

import pytest

from pep8_scanner.core.config import (
    DEFAULT_CONFIG,
    ScanConfig,
    apply_severity_override,
    filter_rules,
    load_config,
)
from pep8_scanner.rules.base import BaseRule, Severity

REPO_ROOT = Path(__file__).resolve().parents[2]


def ecrire_config(tmp_path, contenu):
    fichier = tmp_path / "config.json"
    fichier.write_text(json.dumps(contenu))
    return fichier


class RegleFactice(BaseRule):
    code = "X001"
    severity = Severity.MINEUR

    def check(self, context):
        return []


class AutreRegleFactice(BaseRule):
    code = "X002"
    severity = Severity.MAJEUR

    def check(self, context):
        return []


def test_load_config_sans_filepath_retourne_config_par_defaut():
    assert load_config() == DEFAULT_CONFIG
    assert load_config() == ScanConfig(ignored_rules=frozenset(), severity_overrides={})


def test_load_config_parse_ignored_rules_et_severity_overrides(tmp_path):
    fichier = ecrire_config(
        tmp_path,
        {"ignored_rules": ["W391", "E501"], "severity_overrides": {"E302": 8}},
    )

    config = load_config(fichier)

    assert config.ignored_rules == frozenset({"W391", "E501"})
    assert config.severity_overrides == {"E302": Severity.CRITIQUE}


def test_load_config_rejette_ignored_rules_de_mauvais_type(tmp_path):
    fichier = ecrire_config(tmp_path, {"ignored_rules": "E501"})

    with pytest.raises(ValueError):
        load_config(fichier)


def test_load_config_rejette_poids_de_gravite_invalide(tmp_path):
    fichier = ecrire_config(tmp_path, {"severity_overrides": {"E501": 3}})

    with pytest.raises(ValueError):
        load_config(fichier)


def test_load_config_rejette_booleen_comme_poids(tmp_path):
    fichier = ecrire_config(tmp_path, {"severity_overrides": {"E501": True}})

    with pytest.raises(ValueError):
        load_config(fichier)


def test_load_config_du_fichier_par_defaut_du_depot_est_valide():
    config = load_config(REPO_ROOT / "config" / "default_config.json")

    assert config == DEFAULT_CONFIG


def test_filter_rules_exclut_les_codes_ignores():
    config = load_config()._replace(ignored_rules=frozenset({"X001"}))

    resultat = filter_rules([RegleFactice, AutreRegleFactice], config)

    assert resultat == [AutreRegleFactice]


def test_apply_severity_override_modifie_linstance_sans_toucher_la_classe():
    config = load_config()._replace(
        severity_overrides={"X001": Severity.CRITIQUE}
    )
    rule = RegleFactice()

    apply_severity_override(rule, config)

    assert rule.severity == Severity.CRITIQUE
    assert RegleFactice.severity == Severity.MINEUR


def test_apply_severity_override_ne_change_rien_si_absent():
    config = load_config()
    rule = RegleFactice()

    apply_severity_override(rule, config)

    assert rule.severity == Severity.MINEUR
