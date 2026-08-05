from pep8_scanner.rules.pep8.statements import (
    E711ComparaisonANoneRule,
    E722ExceptNuRule,
)


def test_comparaison_is_none_est_conforme(make_context):
    context = make_context("x = None\nif x is None:\n    pass\n")

    assert E711ComparaisonANoneRule().check(context) == []


def test_comparaison_egalite_a_none_est_detectee(make_context):
    context = make_context("x = None\nif x == None:\n    pass\n")

    violations = E711ComparaisonANoneRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E711"


def test_comparaison_inegalite_a_none_est_detectee(make_context):
    context = make_context("x = None\nif x != None:\n    pass\n")

    violations = E711ComparaisonANoneRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E711"


def test_comparaison_sans_none_est_conforme(make_context):
    context = make_context("x = 1\nif x == 1:\n    pass\n")

    assert E711ComparaisonANoneRule().check(context) == []


def test_except_avec_type_est_conforme(make_context):
    source = "try:\n    pass\nexcept ValueError:\n    pass\n"
    context = make_context(source)

    assert E722ExceptNuRule().check(context) == []


def test_except_nu_est_detecte(make_context):
    source = "try:\n    pass\nexcept:\n    pass\n"
    context = make_context(source)

    violations = E722ExceptNuRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E722"
