"""Règles E711/E722 (cf. CATALOGUE_REGLES.md, section 6 - Instructions et
bonnes pratiques)."""

import ast
from typing import List

from pep8_scanner.rules.base import BaseRule, Severity, Violation
from pep8_scanner.rules.registry import registry

# ast.NameConstant a été retiré en Python 3.9+ (les littéraux None/True/False
# sont représentés par ast.Constant). On garde les deux pour la compatibilité
# 3.6+ visée par le projet (cf. ARCHITECTURE.md).
_NONE_NODE_TYPES = tuple(
    t for t in (ast.Constant, getattr(ast, "NameConstant", None)) if t is not None
)


def _est_constante_none(node) -> bool:
    return isinstance(node, _NONE_NODE_TYPES) and node.value is None


@registry.register(profile="pep8")
class E711ComparaisonANoneRule(BaseRule):

    code = "E711"
    name = "comparaison_a_none"
    description = "Comparaison à None sans 'is'"
    severity = Severity.MAJEUR
    category = "instructions_et_bonnes_pratiques"

    def check(self, context) -> List[Violation]:
        violations = []
        for node in ast.walk(context.tree):
            if not isinstance(node, ast.Compare):
                continue

            operandes = [node.left] + list(node.comparators)
            for index, op in enumerate(node.ops):
                gauche, droite = operandes[index], operandes[index + 1]
                if isinstance(op, (ast.Eq, ast.NotEq)) and (
                    _est_constante_none(gauche) or _est_constante_none(droite)
                ):
                    violations.append(
                        Violation(
                            rule_code=self.code,
                            line=node.lineno,
                            column=node.col_offset + 1,
                            message=(
                                "comparaison à None avec '==' ou '!=' "
                                "au lieu de 'is'/'is not'"
                            ),
                            severity=self.severity,
                        )
                    )
        return violations


@registry.register(profile="pep8")
class E722ExceptNuRule(BaseRule):

    code = "E722"
    name = "except_nu"
    description = "'except:' nu (sans type d'exception)"
    severity = Severity.CRITIQUE
    category = "instructions_et_bonnes_pratiques"

    def check(self, context) -> List[Violation]:
        violations = []
        for node in ast.walk(context.tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=node.lineno,
                        column=node.col_offset + 1,
                        message="'except:' nu, sans type d'exception précisé",
                        severity=self.severity,
                    )
                )
        return violations
