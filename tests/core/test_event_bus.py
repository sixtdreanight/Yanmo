import pytest
from backend.core.event_bus import EventBus


@pytest.mark.asyncio
async def test_emit_and_on():
    bus = EventBus()
    received = []

    async def handler(data):
        received.append(data)

    bus.on("paper.saved", handler)
    await bus.emit("paper.saved", {"id": "1", "title": "Test"})
    await bus.emit("paper.saved", {"id": "2", "title": "Test2"})

    assert len(received) == 2
    assert received[0] == {"id": "1", "title": "Test"}


@pytest.mark.asyncio
async def test_off_unsubscribes():
    bus = EventBus()
    received = []

    async def handler(data):
        received.append(data)

    bus.on("test.event", handler)
    await bus.emit("test.event", {"x": 1})
    bus.off("test.event", handler)
    await bus.emit("test.event", {"x": 2})

    assert len(received) == 1


@pytest.mark.asyncio
async def test_multiple_handlers_same_event():
    bus = EventBus()
    results = []

    async def h1(data):
        results.append(f"h1:{data}")

    async def h2(data):
        results.append(f"h2:{data}")

    bus.on("ev", h1)
    bus.on("ev", h2)
    await bus.emit("ev", "x")

    assert results == ["h1:x", "h2:x"]


@pytest.mark.asyncio
async def test_emit_no_handlers_does_not_error():
    bus = EventBus()
    await bus.emit("no.such.event", {})
