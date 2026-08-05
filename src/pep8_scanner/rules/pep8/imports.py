"""Règle E401 (cf. CATALOGUE_REGLES.md, section 4 - Imports)."""

import ast
from typing import List

from pep8_scanner.rules.base import BaseRule, Severity, Violation
from pep8_scanner.rules.registry import registry


@registry.register(profile="pep8")
class E401ImportsMultiplesRule(BaseRule):

    code = "E401"
    name = "imports_multiples"
    description = "Plusieurs imports sur une même ligne"
    severity = Severity.MODERE
    category = "imports"

    def check(self, context) -> List[Violation]:
        violations = []
        for node in ast.walk(context.tree):
            if isinstance(node, ast.Import) and len(node.names) > 1:
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=node.lineno,
                        column=node.col_offset + 1,
                        message="plusieurs imports sur une même ligne",
                        severity=self.severity,
                    )
                )
        return violations
