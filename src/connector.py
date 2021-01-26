import aiohttp


async def get(url: str, token: str):
    headers = {"Authorization": f'Basic {token}'}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=headers) as session:
        session._cleanup_closed_disabled = True
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.text()
    return data
