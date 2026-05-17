"""Lightweight async task scheduler with cron-like recurring jobs."""

import asyncio
import logging
import time
from collections.abc import Callable, Coroutine
from typing import Any

logger = logging.getLogger(__name__)

TaskFunc = Callable[[], Coroutine[Any, Any, None]]


class ScheduledTask:
    def __init__(self, name: str, func: TaskFunc, interval_seconds: int):
        self.name = name
        self._func = func
        self.interval = interval_seconds
        self.last_run: float = 0
        self.running = False
        self.error_count = 0

    async def execute(self) -> None:
        try:
            self.running = True
            await self._func()
            self.last_run = time.time()
            self.error_count = 0
        except Exception:
            self.error_count += 1
            logger.exception("Scheduled task %s failed (error #%d)", self.name, self.error_count)
        finally:
            self.running = False

    @property
    def due(self) -> bool:
        if self.running:
            return False
        if self.last_run == 0:
            return True  # Never run — due immediately
        return (time.time() - self.last_run) >= self.interval

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "interval": self.interval,
            "last_run": self.last_run,
            "running": self.running,
            "error_count": self.error_count,
        }


class TaskScheduler:
    def __init__(self, tick_interval: float = 5.0):
        self._tasks: dict[str, ScheduledTask] = {}
        self._tick = tick_interval
        self._running = False
        self._task: asyncio.Task | None = None

    def add(self, name: str, func: TaskFunc, interval_seconds: int) -> ScheduledTask:
        task = ScheduledTask(name, func, interval_seconds)
        self._tasks[name] = task
        return task

    def remove(self, name: str) -> None:
        self._tasks.pop(name, None)

    def get(self, name: str) -> ScheduledTask | None:
        return self._tasks.get(name)

    def list_tasks(self) -> list[dict[str, Any]]:
        return [t.status() for t in self._tasks.values()]

    async def start(self) -> None:
        self._running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("Scheduler started with %d tasks", len(self._tasks))

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _loop(self) -> None:
        while self._running:
            for task in list(self._tasks.values()):
                if task.due:
                    asyncio.create_task(task.execute())
            await asyncio.sleep(self._tick)

    async def run_once(self, name: str) -> bool:
        task = self._tasks.get(name)
        if not task:
            return False
        await task.execute()
        return True
