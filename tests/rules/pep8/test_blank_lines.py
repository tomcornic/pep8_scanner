from pep8_scanner.rules.pep8.blank_lines import (
    E302LignesVidesAvantDefinitionRule,
    W391LignesVidesFinDeFichierRule,
)


def test_premiere_definition_du_fichier_nest_pas_verifiee(make_context):
    context = make_context("def premiere():\n    pass\n")

    assert E302LignesVidesAvantDefinitionRule().check(context) == []


def test_deux_lignes_vides_avant_definition_est_conforme(make_context):
    source = "def premiere():\n    pass\n\n\ndef seconde():\n    pass\n"
    context = make_context(source)

    assert E302LignesVidesAvantDefinitionRule().check(context) == []


def test_une_seule_ligne_vide_avant_definition_est_detectee(make_context):
    source = "def premiere():\n    pass\n\ndef seconde():\n    pass\n"
    context = make_context(source)

    violations = E302LignesVidesAvantDefinitionRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E302"
    assert violations[0].line == 4


def test_definition_sans_ligne_vide_est_detectee(make_context):
    source = "def premiere():\n    pass\nclass Seconde:\n    pass\n"
    context = make_context(source)

    violations = E302LignesVidesAvantDefinitionRule().check(context)

    assert len(violations) == 1
    assert violations[0].line == 3


def test_definition_decoree_est_verifiee_a_partir_du_decorateur(make_context):
    source = (
        "def premiere():\n"
        "    pass\n"
        "\n"
        "@staticmethod\n"
        "def seconde():\n"
        "    pass\n"
    )
    context = make_context(source)

    violations = E302LignesVidesAvantDefinitionRule().check(context)

    assert len(violations) == 1
    assert violations[0].line == 4


def test_fichier_sans_ligne_vide_finale_est_conforme(make_context):
    context = make_context("x = 1\n")

    assert W391LignesVidesFinDeFichierRule().check(context) == []


def test_fichier_avec_ligne_vide_finale_est_detecte(make_context):
    context = make_context("x = 1\n\n")

    violations = W391LignesVidesFinDeFichierRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "W391"
