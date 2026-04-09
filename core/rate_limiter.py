import asyncio


class RateLimiter:
    def __init__(self, rps: float):
        self._delay = 1.0 / rps
        self._lock = asyncio.Lock()
        self._last_call = 0.0

    async def acquire(self):
        async with self._lock:
            loop = asyncio.get_event_loop()
            now = loop.time()
            gap = self._delay - (now - self._last_call)
            if gap > 0:
                await asyncio.sleep(gap)
            self._last_call = loop.time()
