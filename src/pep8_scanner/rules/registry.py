"""Registre des règles, organisées par profil de normes
(ex: "pep8", "pep257" — cf. ARCHITECTURE.md).
"""

from typing import Dict, List, Optional, Type

from pep8_scanner.rules.base import BaseRule


class RuleRegistry:

    def __init__(self):
        self._rules: Dict[str, Type[BaseRule]] = {}
        self._profiles: Dict[str, List[str]] = {}

    def register(self, profile: str):
        """Décorateur enregistrant une classe de règle dans un profil."""

        def decorator(rule_cls: Type[BaseRule]) -> Type[BaseRule]:
            if not rule_cls.code:
                raise ValueError(
                    "La règle {} doit définir un attribut 'code'.".format(
                        rule_cls.__name__
                    )
                )
            if rule_cls.code in self._rules:
                raise ValueError(
                    "Le code de règle '{}' est déjà enregistré.".format(
                        rule_cls.code
                    )
                )
            self._rules[rule_cls.code] = rule_cls
            self._profiles.setdefault(profile, []).append(rule_cls.code)
            return rule_cls

        return decorator

    def get_rule(self, code: str) -> Type[BaseRule]:
        return self._rules[code]

    def get_rules(self, profile: Optional[str] = None) -> List[Type[BaseRule]]:
        """Retourne les règles d'un profil donné, ou toutes les règles
        enregistrées si aucun profil n'est précisé."""
        if profile is None:
            return list(self._rules.values())
        codes = self._profiles.get(profile, [])
        return [self._rules[code] for code in codes]

    def profiles(self) -> List[str]:
        return list(self._profiles.keys())


registry = RuleRegistry()
