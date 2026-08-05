from pep8_scanner.rules.pep8.blank_lines import (
    E301LigneVideAvantMethodeRule,
    E302LignesVidesAvantDefinitionRule,
    E303TropDeLignesVidesRule,
    W292PasDeRetourLigneFinDeFichierRule,
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


def test_premiere_methode_de_la_classe_nest_pas_verifiee(make_context):
    source = "class C:\n    def premiere(self):\n        pass\n"
    context = make_context(source)

    assert E301LigneVideAvantMethodeRule().check(context) == []


def test_methode_avec_ligne_vide_avant_est_conforme(make_context):
    source = (
        "class C:\n"
        "    def premiere(self):\n"
        "        pass\n"
        "\n"
        "    def seconde(self):\n"
        "        pass\n"
    )
    context = make_context(source)

    assert E301LigneVideAvantMethodeRule().check(context) == []


def test_methode_sans_ligne_vide_avant_est_detectee(make_context):
    source = (
        "class C:\n"
        "    def premiere(self):\n"
        "        pass\n"
        "    def seconde(self):\n"
        "        pass\n"
    )
    context = make_context(source)

    violations = E301LigneVideAvantMethodeRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E301"
    assert violations[0].line == 4


def test_deux_lignes_vides_consecutives_est_conforme(make_context):
    context = make_context("x = 1\n\n\ny = 2\n")

    assert E303TropDeLignesVidesRule().check(context) == []


def test_trois_lignes_vides_consecutives_est_detecte(make_context):
    context = make_context("x = 1\n\n\n\ny = 2\n")

    violations = E303TropDeLignesVidesRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E303"
    assert violations[0].line == 5


def test_fichier_avec_retour_a_la_ligne_final_est_conforme(make_context):
    context = make_context("x = 1\n")

    assert W292PasDeRetourLigneFinDeFichierRule().check(context) == []


def test_fichier_sans_retour_a_la_ligne_final_est_detecte(make_context):
    context = make_context("x = 1")

    violations = W292PasDeRetourLigneFinDeFichierRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "W292"
