"""Règles E301/E302/E303/W391/W292 (cf. CATALOGUE_REGLES.md, section 3 -
Lignes vides)."""

import ast
from typing import List

from pep8_scanner.rules.base import BaseRule, Severity, Violation
from pep8_scanner.rules.registry import registry


def _compter_lignes_vides_avant(lines: List[str], start_line: int) -> int:
    blank_count = 0
    line_index = start_line - 2
    while line_index >= 0 and lines[line_index].strip() == "":
        blank_count += 1
        line_index -= 1
    return blank_count


@registry.register(profile="pep8")
class E301LigneVideAvantMethodeRule(BaseRule):

    code = "E301"
    name = "ligne_vide_avant_methode"
    description = "1 ligne vide attendue avant une méthode, absente"
    severity = Severity.MODERE
    category = "lignes_vides"

    REQUIRED_BLANK_LINES = 1
    METHOD_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)

    def check(self, context) -> List[Violation]:
        violations = []
        for classe in ast.walk(context.tree):
            if not isinstance(classe, ast.ClassDef):
                continue

            methodes = [
                node for node in classe.body if isinstance(node, self.METHOD_TYPES)
            ]

            for index, methode in enumerate(methodes):
                if index == 0:
                    continue

                start_line = (
                    methode.decorator_list[0].lineno
                    if methode.decorator_list
                    else methode.lineno
                )
                blank_count = _compter_lignes_vides_avant(context.lines, start_line)

                if blank_count < self.REQUIRED_BLANK_LINES:
                    violations.append(
                        Violation(
                            rule_code=self.code,
                            line=start_line,
                            column=1,
                            message=(
                                "{} ligne(s) vide(s) trouvée(s), "
                                "1 attendue avant '{}'"
                            ).format(blank_count, methode.name),
                            severity=self.severity,
                        )
                    )
        return violations


@registry.register(profile="pep8")
class E303TropDeLignesVidesRule(BaseRule):

    code = "E303"
    name = "trop_de_lignes_vides"
    description = "Trop de lignes vides consécutives"
    severity = Severity.MINEUR
    category = "lignes_vides"

    MAX_BLANK_LINES = 2

    def check(self, context) -> List[Violation]:
        violations = []
        blank_count = 0
        for line_number, line in enumerate(context.lines, start=1):
            if line.strip() == "":
                blank_count += 1
                continue
            if blank_count > self.MAX_BLANK_LINES:
                violations.append(
                    Violation(
                        rule_code=self.code,
                        line=line_number,
                        column=1,
                        message="trop de lignes vides consécutives ({})".format(
                            blank_count
                        ),
                        severity=self.severity,
                    )
                )
            blank_count = 0
        return violations


@registry.register(profile="pep8")
class W292PasDeRetourLigneFinDeFichierRule(BaseRule):

    code = "W292"
    name = "pas_de_retour_ligne_fin_de_fichier"
    description = "Pas de retour à la ligne en fin de fichier"
    severity = Severity.MINEUR
    category = "lignes_vides"

    def check(self, context) -> List[Violation]:
        if context.source and not context.source.endswith("\n"):
            derniere_ligne = context.lines[-1] if context.lines else ""
            return [
                Violation(
                    rule_code=self.code,
                    line=len(context.lines) or 1,
                    column=len(derniere_ligne) + 1,
                    message="pas de retour à la ligne en fin de fichier",
                    severity=self.severity,
                )
            ]
        return []


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

            blank_count = _compter_lignes_vides_avant(context.lines, start_line)

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
