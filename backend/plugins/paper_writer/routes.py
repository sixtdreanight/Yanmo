from fastapi import APIRouter
from pydantic import BaseModel
from backend.plugins.paper_writer.outline import generate_outline
from backend.plugins.paper_writer.citation import parse_bibtex


class OutlineRequest(BaseModel):
    topic: str


class BibtexRequest(BaseModel):
    bibtex: str


def create_router(plugin) -> APIRouter:
    router = APIRouter(prefix="/api/paper-writer", tags=["paper-writer"])

    @router.post("/outline")
    async def outline(req: OutlineRequest):
        sections = generate_outline(req.topic)
        return {
            "sections": [
                {"title": s.title, "key_points": s.key_points, "estimated_words": s.estimated_words}
                for s in sections
            ]
        }

    @router.post("/citation/parse")
    async def parse_citation(req: BibtexRequest):
        entries = parse_bibtex(req.bibtex)
        return {
            "entries": [
                {"cite_key": e.cite_key, "title": e.title, "author": e.author,
                 "year": e.year, "journal": e.journal or e.booktitle}
                for e in entries
            ]
        }

    return router
