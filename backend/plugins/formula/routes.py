from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.formula.verify import verify_formula, sympy_verify, latex_to_sympy


class VerifyRequest(BaseModel):
    expression: str
    domain: str = "real"


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/formula", tags=["formula"])

    @router.post("/verify")
    async def verify(req: VerifyRequest):
        basic = verify_formula(req.expression, req.domain)
        sympy_result = sympy_verify(req.expression)
        return {
            "basic": {
                "is_valid": basic.is_valid,
                "errors": basic.errors,
                "warnings": basic.warnings,
                "suggestions": basic.suggestions,
            },
            "sympy": {
                "is_valid": sympy_result.is_valid,
                "errors": sympy_result.errors,
                "suggestions": sympy_result.suggestions,
            },
            "cross_validated": basic.is_valid and sympy_result.is_valid,
        }

    @router.post("/convert")
    async def convert_latex(data: dict):
        latex_str = data.get("latex", "")
        python_expr = latex_to_sympy(latex_str)
        return {"python": python_expr}

    return router
