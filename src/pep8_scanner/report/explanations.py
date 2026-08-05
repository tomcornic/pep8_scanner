"""Textes explicatifs et correctifs pré-écrits par règle
(cf. ARCHITECTURE.md, readme.md - pas de génération dynamique via IA)."""

from typing import NamedTuple, Optional

from pep8_scanner.rules.base import Violation


class Explanation(NamedTuple):
    summary: str
    why: str
    example_incorrect: str
    example_correct: str


EXPLANATIONS = {
    "E501": Explanation(
        summary="Ligne trop longue (> 79 caractères).",
        why=(
            "Le PEP 8 recommande de limiter les lignes à 79 caractères pour "
            "rester lisible sur des affichages côte à côte (diffs, revues "
            "de code, terminaux) et éviter le retour à la ligne automatique."
        ),
        example_incorrect=(
            "resultat = fonction_avec_un_nom_tres_long("
            "argument_un, argument_deux, argument_trois)"
        ),
        example_correct=(
            "resultat = fonction_avec_un_nom_tres_long(\n"
            "    argument_un, argument_deux, argument_trois\n"
            ")"
        ),
    ),
    "W291": Explanation(
        summary="Espace(s) superflu(s) en fin de ligne.",
        why=(
            "Les espaces en fin de ligne sont invisibles mais polluent les "
            "diffs git (chaque ligne modifiée sans raison apparente) et "
            "n'ont aucune utilité."
        ),
        example_incorrect="x = 1   \n",
        example_correct="x = 1\n",
    ),
    "W293": Explanation(
        summary="Espace(s) sur une ligne censée être vide.",
        why=(
            "Une ligne vide contenant des espaces n'est pas réellement "
            "vide : elle génère le même bruit inutile dans les diffs que "
            "W291."
        ),
        example_incorrect="def f():\n    pass\n   \ndef g():\n    pass\n",
        example_correct="def f():\n    pass\n\ndef g():\n    pass\n",
    ),
    "E302": Explanation(
        summary="2 lignes vides attendues avant une fonction/classe top-level.",
        why=(
            "Le PEP 8 impose 2 lignes vides avant chaque définition de "
            "fonction ou de classe au niveau module, pour séparer "
            "visuellement les blocs de code indépendants."
        ),
        example_incorrect="def premiere():\n    pass\ndef seconde():\n    pass\n",
        example_correct=(
            "def premiere():\n    pass\n\n\ndef seconde():\n    pass\n"
        ),
    ),
    "W391": Explanation(
        summary="Ligne(s) vide(s) en fin de fichier.",
        why=(
            "Le PEP 8 recommande qu'un fichier se termine par une seule "
            "nouvelle ligne, sans lignes vides superflues à la fin."
        ),
        example_incorrect="x = 1\n\n\n",
        example_correct="x = 1\n",
    ),
}


def get_explanation(rule_code: str) -> Optional[Explanation]:
    return EXPLANATIONS.get(rule_code)


def explain_violation(violation: Violation) -> str:
    """Formate un texte complet (constat + pourquoi + exemple de
    correction) pour une infraction donnée. Se rabat sur le message brut
    de la règle si aucune explication n'est encore écrite pour son code
    (catalogue en cours de complétion, cf. CATALOGUE_REGLES.md)."""
    explanation = get_explanation(violation.rule_code)
    if explanation is None:
        return "{} (ligne {}) : {}".format(
            violation.rule_code, violation.line, violation.message
        )

    return (
        "{code} (ligne {line}) : {summary}\n"
        "Pourquoi : {why}\n"
        "Incorrect :\n{incorrect}\n"
        "Correct :\n{correct}"
    ).format(
        code=violation.rule_code,
        line=violation.line,
        summary=explanation.summary,
        why=explanation.why,
        incorrect=explanation.example_incorrect,
        correct=explanation.example_correct,
    )
