import asyncio
from collections import defaultdict
from collections.abc import Callable, Coroutine
from typing import Any

Handler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def on(self, event: str, handler: Handler) -> None:
        self._handlers[event].append(handler)

    def off(self, event: str, handler: Handler) -> None:
        if event in self._handlers:
            self._handlers[event] = [
                h for h in self._handlers[event] if h is not handler
            ]

    async def emit(self, event: str, data: dict[str, Any]) -> None:
        handlers = self._handlers.get(event, [])
        tasks = [handler(data) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
