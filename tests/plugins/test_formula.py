import pytest
from backend.plugins.formula.verify import verify_formula, FormulaVerification


def test_verify_quadratic_formula():
    result = verify_formula(expression="(-b + sqrt(b**2 - 4*a*c)) / (2*a)", domain="real")
    assert isinstance(result, FormulaVerification)
    assert result.is_valid


def test_verify_division_by_zero_detected():
    result = verify_formula(expression="1 / 0", domain="real")
    assert result.is_valid is False
    assert len(result.errors) >= 1


def test_plugin_declaration():
    from backend.plugins.formula.plugin import FormulaPlugin
    plugin = FormulaPlugin()
    assert plugin.name == "formula"
    assert plugin.display_name == "验公式"
