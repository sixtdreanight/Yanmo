from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.plugins.term_advisor.advisor import parse_advisor_text, create_plan


class ParseRequest(BaseModel):
    text: str


class PlanRequest(BaseModel):
    text: str
    title: str = ""


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/term-advisor", tags=["term-advisor"])

    @router.post("/parse")
    async def parse_advisor(req: ParseRequest):
        tasks = parse_advisor_text(req.text)
        return {
            "tasks": [
                {"action": t.action, "keywords": t.keywords, "priority": t.priority}
                for t in tasks
            ]
        }

    @router.post("/plan")
    async def plan_advisor(req: PlanRequest):
        tasks = parse_advisor_text(req.text)
        plan = create_plan(tasks, req.title)
        return {
            "title": plan.title,
            "total_days_min": plan.total_days_min,
            "total_days_max": plan.total_days_max,
            "tasks": [
                {
                    "index": t.index,
                    "action": t.action,
                    "keywords": t.keywords,
                    "phase": t.phase.value,
                    "estimated_days_min": t.estimated_days_min,
                    "estimated_days_max": t.estimated_days_max,
                    "depends_on": t.depends_on,
                    "subtasks": t.subtasks,
                    "resources": t.resources,
                    "milestone": t.milestone,
                }
                for t in plan.tasks
            ],
            "timeline": plan.timeline,
        }

    @router.get("/commands")
    async def get_commands():
        return {"commands": plugin.get_commands()}

    return router
