import ast

# Déclenche l'enregistrement des règles dans le registre global, pour que
# ce module de test soit indépendant de l'ordre de collecte de pytest.
import pep8_scanner.rules.pep8.blank_lines  # noqa: F401
import pep8_scanner.rules.pep8.line_length  # noqa: F401
import pep8_scanner.rules.pep8.whitespace  # noqa: F401
from pep8_scanner.core.analyzer import analyze_file, build_context


def test_build_context_reads_file_and_parses_ast(tmp_path):
    fichier = tmp_path / "module.py"
    fichier.write_text("x = 1\n")

    context = build_context(fichier)

    assert context.source == "x = 1\n"
    assert context.lines == ["x = 1"]
    assert isinstance(context.tree, ast.Module)
    assert len(context.tokens) > 0


def test_analyze_file_detects_violations_on_disk(tmp_path):
    fichier = tmp_path / "module.py"
    fichier.write_text("x = 1   \ny = 2  # " + ("a" * 80) + "\n")

    violations = analyze_file(fichier, profile="pep8")

    codes = {v.rule_code for v in violations}
    assert "W291" in codes
    assert "E501" in codes


def test_analyze_file_returns_empty_list_for_conform_code(tmp_path):
    fichier = tmp_path / "module.py"
    fichier.write_text(
        "def premiere():\n"
        "    pass\n"
        "\n"
        "\n"
        "def seconde():\n"
        "    pass\n"
    )

    violations = analyze_file(fichier, profile="pep8")

    assert violations == []


def test_analyze_file_without_profile_runs_all_registered_rules(tmp_path):
    fichier = tmp_path / "module.py"
    fichier.write_text("x = 1  # " + ("a" * 80) + "\n")

    violations = analyze_file(fichier)

    assert any(v.rule_code == "E501" for v in violations)
