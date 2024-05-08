# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from cogs.user_greeting import Greetings
from cogs.error_handler import ErrorHandler
from cogs.chabot import ChatBot

cogs = [Greetings, ErrorHandler, ChatBot]

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    for cog in cogs:
        await bot.add_cog(cog(bot))

bot.run(getenv("DISCORD_BOT_TOKEN"))
