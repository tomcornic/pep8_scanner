from pep8_scanner.rules.pep8.whitespace import (
    W291EspaceFinDeLigneRule,
    W293EspaceSurLigneVideRule,
)


def test_ligne_sans_espace_final_est_conforme(make_context):
    context = make_context("x = 1\n")

    assert W291EspaceFinDeLigneRule().check(context) == []


def test_ligne_avec_espace_final_est_detectee(make_context):
    context = make_context("x = 1   \ny = 2\n")

    violations = W291EspaceFinDeLigneRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "W291"
    assert violations[0].line == 1


def test_ligne_vide_ordinaire_ne_declenche_pas_w291(make_context):
    context = make_context("x = 1\n\ny = 2\n")

    assert W291EspaceFinDeLigneRule().check(context) == []


def test_ligne_vide_avec_espaces_est_detectee_w293(make_context):
    context = make_context("x = 1\n   \ny = 2\n")

    violations = W293EspaceSurLigneVideRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "W293"
    assert violations[0].line == 2


def test_ligne_vide_avec_espaces_ne_declenche_pas_w291(make_context):
    context = make_context("x = 1\n   \ny = 2\n")

    assert W291EspaceFinDeLigneRule().check(context) == []
