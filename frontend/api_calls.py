import aiohttp

async def fetch_clips(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://127.0.0.1:8000/clips",
            params={"query": query},
        ) as response:
            return await response.json()
        
async def fetch_slides(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://127.0.0.1:8000/slides",
            params={"query": query},
        ) as response:
            return await response.json()