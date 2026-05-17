import re
from dataclasses import dataclass, field


@dataclass
class FormulaVerification:
    expression: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def verify_formula(expression: str, domain: str = "real") -> FormulaVerification:
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    paren_count = 0
    for ch in expression:
        if ch in "([{":
            paren_count += 1
        elif ch in ")]}":
            paren_count -= 1
        if paren_count < 0:
            errors.append("括号不匹配")
            break
    if paren_count > 0:
        errors.append("括号不匹配")
    if paren_count == 0 and not errors:
        suggestions.append("括号匹配正确")

    if re.search(r"/\s*0\b", expression):
        errors.append("除零错误")

    if domain == "real":
        neg_sqrt = re.findall(r"sqrt\s*\(\s*-", expression)
        if neg_sqrt:
            warnings.append("实数域下 sqrt 参数可能为负，请确认定义域")

    if "\\" in expression:
        suggestions.append("检测到 LaTeX 命令，将转换为 SymPy 可解析格式")

    is_valid = len(errors) == 0
    return FormulaVerification(
        expression=expression,
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
    )


def latex_to_sympy(latex_str: str) -> str:
    s = latex_str
    s = s.replace("\\frac{", "(").replace("}{", ")/(").replace("}", ")")
    s = s.replace("\\sqrt", "sqrt")
    s = s.replace("\\sum", "Sum")
    s = s.replace("\\int", "Integral")
    s = s.replace("\\alpha", "alpha")
    s = s.replace("\\beta", "beta")
    s = s.replace("\\theta", "theta")
    s = s.replace("\\pi", "pi")
    s = s.replace("\\infty", "oo")
    s = s.replace("\\cdot", "*")
    s = s.replace("^", "**")
    s = s.replace("{", "(").replace("}", ")")
    return s


def sympy_verify(latex_str: str) -> FormulaVerification:
    errors: list[str] = []
    suggestions: list[str] = []

    try:
        import sympy
        python_expr = latex_to_sympy(latex_str)
        sympy_parsed = sympy.sympify(python_expr)
        suggestions.append(f"SymPy 解析成功: {sympy_parsed}")
    except Exception as e:
        errors.append(f"SymPy 解析失败: {str(e)[:100]}")
        return FormulaVerification(expression=latex_str, is_valid=False, errors=errors)

    symbols = list(sympy_parsed.free_symbols) if hasattr(sympy_parsed, 'free_symbols') else []
    if symbols:
        suggestions.append(f"检测到符号: {', '.join(str(s) for s in symbols)}")

    is_valid = len(errors) == 0
    return FormulaVerification(
        expression=latex_str,
        is_valid=is_valid,
        errors=errors,
        warnings=[],
        suggestions=suggestions,
    )
