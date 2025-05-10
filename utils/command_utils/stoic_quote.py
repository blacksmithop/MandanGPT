import aiohttp
from utils import StoicQuote


async def fetch_stoic_quote():
    url = "https://stoic.tekloon.net/stoic-quote"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                quote = StoicQuote(**data)
                return quote
            else:
                raise Exception(f"Failed to fetch quote: HTTP {response.status}")
