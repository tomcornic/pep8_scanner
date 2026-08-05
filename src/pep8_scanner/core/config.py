"""Chargement et validation du fichier de configuration JSON
(cf. ARCHITECTURE.md, readme.md - personnalisation : ignorer des règles
ou ajuster leur poids de gravité)."""

import json
from pathlib import Path
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Type

from pep8_scanner.rules.base import BaseRule, Severity

VALID_SEVERITY_WEIGHTS = {s.value for s in Severity}


class ScanConfig(NamedTuple):
    ignored_rules: FrozenSet[str]
    severity_overrides: Dict[str, Severity]


DEFAULT_CONFIG = ScanConfig(ignored_rules=frozenset(), severity_overrides={})


def load_config(filepath: Optional[str] = None) -> ScanConfig:
    """Charge et valide un fichier de configuration JSON. Retourne une
    configuration vide (aucune personnalisation) si `filepath` est
    None."""
    if filepath is None:
        return DEFAULT_CONFIG

    with Path(filepath).open(encoding="utf-8") as f:
        data = json.load(f)

    return _parse_config(data)


def _parse_config(data) -> ScanConfig:
    if not isinstance(data, dict):
        raise ValueError(
            "Le fichier de configuration doit contenir un objet JSON."
        )

    ignored_rules_raw = data.get("ignored_rules", [])
    if not isinstance(ignored_rules_raw, list) or not all(
        isinstance(code, str) for code in ignored_rules_raw
    ):
        raise ValueError(
            "'ignored_rules' doit être une liste de codes de règle (chaînes)."
        )

    severity_overrides_raw = data.get("severity_overrides", {})
    if not isinstance(severity_overrides_raw, dict):
        raise ValueError(
            "'severity_overrides' doit être un objet {code_regle: poids}."
        )

    severity_overrides = {}
    for code, poids in severity_overrides_raw.items():
        if isinstance(poids, bool) or poids not in VALID_SEVERITY_WEIGHTS:
            raise ValueError(
                "Poids de gravité invalide pour '{}' : {} (attendu un "
                "parmi {}).".format(code, poids, sorted(VALID_SEVERITY_WEIGHTS))
            )
        severity_overrides[code] = Severity(poids)

    return ScanConfig(
        ignored_rules=frozenset(ignored_rules_raw),
        severity_overrides=severity_overrides,
    )


def filter_rules(
    rule_classes: List[Type[BaseRule]], config: ScanConfig
) -> List[Type[BaseRule]]:
    """Exclut les règles listées dans `config.ignored_rules`."""
    return [rc for rc in rule_classes if rc.code not in config.ignored_rules]


def apply_severity_override(rule: BaseRule, config: ScanConfig) -> BaseRule:
    """Applique, si présent, le poids de gravité personnalisé de la
    config sur une instance de règle (avant l'appel à check())."""
    override = config.severity_overrides.get(rule.code)
    if override is not None:
        rule.severity = override
    return rule
