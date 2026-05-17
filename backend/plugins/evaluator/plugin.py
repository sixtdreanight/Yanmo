from fastapi import APIRouter


class EvaluatorPlugin:
    name = "evaluator"
    display_name = "审项目"
    version = "0.1.0"

    async def on_load(self, bus, config):
        self._bus = bus
        self._config = config

    async def on_unload(self):
        pass

    def get_routes(self) -> APIRouter:
        from backend.plugins.evaluator.routes import create_router
        return create_router(self)

    def get_commands(self) -> list:
        return ["/evaluate"]

Plugin = EvaluatorPlugin
