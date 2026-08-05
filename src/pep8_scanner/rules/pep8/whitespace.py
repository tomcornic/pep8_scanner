"""Règles W291/W293 (cf. CATALOGUE_REGLES.md, section 2 - Espacement)."""

from typing import List

from pep8_scanner.rules.base import BaseRule, Severity, Violation
from pep8_scanner.rules.registry import registry


@registry.register(profile="pep8")
class W291EspaceFinDeLigneRule(BaseRule):

    code = "W291"
    name = "espace_fin_de_ligne"
    description = "Espace en fin de ligne"
    severity = Severity.MINEUR
    category = "espacement"

    def check(self, context) -> List[Violation]:
        violations = []
        for line_number, line in enumerate(context.lines, start=1):
            if line.strip() != "" and line != line.rstrip():
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=line_number,
                        column=len(line.rstrip()) + 1,
                        message="espace(s) superflu(s) en fin de ligne",
                        severity=self.severity,
                    )
                )
        return violations


@registry.register(profile="pep8")
class W293EspaceSurLigneVideRule(BaseRule):

    code = "W293"
    name = "espace_sur_ligne_vide"
    description = "Espace sur une ligne vide"
    severity = Severity.MINEUR
    category = "espacement"

    def check(self, context) -> List[Violation]:
        violations = []
        for line_number, line in enumerate(context.lines, start=1):
            if line != "" and line.strip() == "":
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=line_number,
                        column=1,
                        message="espace(s) sur une ligne vide",
                        severity=self.severity,
                    )
                )
        return violations
