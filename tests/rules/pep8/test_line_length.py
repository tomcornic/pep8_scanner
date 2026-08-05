from pep8_scanner.rules.pep8.line_length import E501LigneTropLongueRule


def test_ligne_conforme_ne_declenche_rien(make_context):
    source = "x = 1\n"
    context = make_context(source)

    violations = E501LigneTropLongueRule().check(context)

    assert violations == []


def test_ligne_trop_longue_est_detectee(make_context):
    source = "x = 1  # " + ("a" * 80) + "\n"
    context = make_context(source)

    violations = E501LigneTropLongueRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E501"
    assert violations[0].line == 1
