from collections.abc import AsyncIterable

import aiohttp
from dishka import Provider, Scope, provide


class HttpProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_http_session(self) -> AsyncIterable[aiohttp.ClientSession]:
        session = aiohttp.ClientSession()
        yield session
        await session.close()
