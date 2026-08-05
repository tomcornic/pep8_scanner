"""Contexte d'analyse transmis aux règles (cf. ARCHITECTURE.md)."""


class AnalysisContext:
    """Regroupe, pour un fichier donné, tout ce dont une règle a besoin
    pour effectuer sa vérification : source brut, arbre AST et flux de
    tokens (nécessaires pour les écarts non visibles dans l'AST, ex:
    espacement).
    """

    def __init__(self, filepath, source, tree, tokens):
        self.filepath = filepath
        self.source = source
        self.lines = source.splitlines()
        self.tree = tree
        self.tokens = tokens
