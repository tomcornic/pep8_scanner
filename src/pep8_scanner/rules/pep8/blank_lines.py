"""Règles E302/W391 (cf. CATALOGUE_REGLES.md, section 3 - Lignes vides)."""

import ast
from typing import List

from pep8_scanner.rules.base import BaseRule, Severity, Violation
from pep8_scanner.rules.registry import registry


@registry.register(profile="pep8")
class E302LignesVidesAvantDefinitionRule(BaseRule):

    code = "E302"
    name = "lignes_vides_avant_definition_top_level"
    description = "2 lignes vides attendues avant une fonction/classe top-level"
    severity = Severity.MODERE
    category = "lignes_vides"

    REQUIRED_BLANK_LINES = 2
    TOP_LEVEL_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)

    def check(self, context) -> List[Violation]:
        violations = []
        top_level_nodes = [
            node for node in context.tree.body
            if isinstance(node, self.TOP_LEVEL_TYPES)
        ]

        for index, node in enumerate(top_level_nodes):
            if index == 0:
                continue

            start_line = (
                node.decorator_list[0].lineno
                if node.decorator_list
                else node.lineno
            )

            blank_count = 0
            line_index = start_line - 2
            while line_index >= 0 and context.lines[line_index].strip() == "":
                blank_count += 1
                line_index -= 1

            if blank_count < self.REQUIRED_BLANK_LINES:
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=start_line,
                        column=1,
                        message=(
                            "{} ligne(s) vide(s) trouvée(s), "
                            "2 attendues avant '{}'"
                        ).format(blank_count, node.name),
                        severity=self.severity,
                    )
                )
        return violations


@registry.register(profile="pep8")
class W391LignesVidesFinDeFichierRule(BaseRule):

    code = "W391"
    name = "lignes_vides_fin_de_fichier"
    description = "Ligne(s) vide(s) en fin de fichier"
    severity = Severity.MINEUR
    category = "lignes_vides"

    def check(self, context) -> List[Violation]:
        lines = context.lines
        if lines and lines[-1].strip() == "":
            return [
                Violation(
                    rule_code=self.code,
                    line=len(lines),
                    column=1,
                    message="ligne(s) vide(s) en fin de fichier",
                    severity=self.severity,
                )
            ]
        return []
