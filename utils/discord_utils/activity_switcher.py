import discord
from utils import fetch_stoic_quote, StoicQuote


async def get_new_activity():
    quote_data: StoicQuote = await fetch_stoic_quote()
    quote = quote_data.data.quote

    new_activity = discord.Activity(
        type=discord.ActivityType.playing,
        name=quote,
        # state=quote,
        # assets={
        #     "large_image": "image3",
        #     "large_text": "Galaxy View",
        # },
    )
    return new_activity
