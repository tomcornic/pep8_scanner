from pep8_scanner.rules.pep8.imports import E401ImportsMultiplesRule


def test_import_unique_est_conforme(make_context):
    context = make_context("import os\n")

    assert E401ImportsMultiplesRule().check(context) == []


def test_imports_multiples_sur_une_ligne_est_detecte(make_context):
    context = make_context("import os, sys\n")

    violations = E401ImportsMultiplesRule().check(context)

    assert len(violations) == 1
    assert violations[0].rule_code == "E401"


def test_from_import_multiple_nest_pas_concerne(make_context):
    context = make_context("from os import path, sep\n")

    assert E401ImportsMultiplesRule().check(context) == []
