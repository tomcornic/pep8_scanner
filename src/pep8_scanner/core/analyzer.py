"""Orchestration ast + tokenize par fichier (cf. ARCHITECTURE.md)."""

import ast
import io
import tokenize
from pathlib import Path
from typing import List, Optional

from pep8_scanner.core.context import AnalysisContext
from pep8_scanner.rules.base import Violation
from pep8_scanner.rules.registry import registry


def build_context(filepath) -> AnalysisContext:
    """Lit un fichier .py et construit son AnalysisContext (source, AST,
    tokens). L'encodage est détecté via la déclaration PEP 263
    (`tokenize.open`), avec repli sur UTF-8.
    """
    path = Path(filepath)
    with tokenize.open(path) as f:
        source = f.read()
    tree = ast.parse(source, filename=str(path))
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    return AnalysisContext(
        filepath=str(path), source=source, tree=tree, tokens=tokens
    )


def run_rules(context: AnalysisContext, profile: Optional[str] = None) -> List[Violation]:
    """Exécute contre un AnalysisContext déjà construit toutes les règles
    du profil donné (ou toutes les règles enregistrées si `profile` est
    None)."""
    violations: List[Violation] = []
    for rule_cls in registry.get_rules(profile=profile):
        violations.extend(rule_cls().check(context))
    return violations


def analyze_file(filepath, profile: Optional[str] = None) -> List[Violation]:
    """Construit l'AnalysisContext du fichier puis exécute les règles
    contre lui (cf. `run_rules`)."""
    context = build_context(filepath)
    return run_rules(context, profile=profile)
