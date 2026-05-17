from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.evaluator.evaluate import evaluate_project


class EvalRequest(BaseModel):
    title: str
    description: str
    field: str = ""


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/evaluator", tags=["evaluator"])

    @router.post("/evaluate")
    async def evaluate(req: EvalRequest):
        result = evaluate_project(req.title, req.description, req.field)
        return {
            "title": result.title,
            "innovation_score": result.innovation_score,
            "rationality_score": result.rationality_score,
            "methodology_score": result.methodology_score,
            "strengths": result.strengths,
            "weaknesses": result.weaknesses,
            "suggestions": result.suggestions,
        }

    return router
