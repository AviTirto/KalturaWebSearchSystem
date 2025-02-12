import aiohttp

async def fetch_clips(query: str, key: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://127.0.0.1:8000/",
            params={"query": query, "key": key},
        ) as response:
            return await response.json()