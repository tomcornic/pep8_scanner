import ast
import io
import tokenize

import pytest

from pep8_scanner.core.context import AnalysisContext


@pytest.fixture
def make_context():
    def _make_context(source, filepath="test.py"):
        tree = ast.parse(source)
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
        return AnalysisContext(
            filepath=filepath, source=source, tree=tree, tokens=tokens
        )

    return _make_context
