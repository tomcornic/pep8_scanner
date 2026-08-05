"""Règle E501 (cf. CATALOGUE_REGLES.md, section 5 - Longueur de ligne)."""

from typing import List

from pep8_scanner.rules.base import BaseRule, Severity, Violation
from pep8_scanner.rules.registry import registry


@registry.register(profile="pep8")
class E501LigneTropLongueRule(BaseRule):

    code = "E501"
    name = "ligne_trop_longue"
    description = "Ligne trop longue (> 79 caractères)"
    severity = Severity.MODERE
    category = "longueur_de_ligne"

    MAX_LINE_LENGTH = 79

    def check(self, context) -> List[Violation]:
        violations = []
        for line_number, line in enumerate(context.lines, start=1):
            length = len(line)
            if length > self.MAX_LINE_LENGTH:
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=line_number,
                        column=self.MAX_LINE_LENGTH + 1,
                        message="ligne trop longue ({} > {} caractères)".format(
                            length, self.MAX_LINE_LENGTH
                        ),
                        severity=self.severity,
                    )
                )
        return violations
