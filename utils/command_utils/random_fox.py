import aiohttp
from utils import RandomFox


async def fetch_random_fox():
    url = "https://randomfox.ca/floof"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                quote = RandomFox(**data)
                return quote
            else:
                raise Exception(f"Failed to fetch fox image: HTTP {response.status}")
