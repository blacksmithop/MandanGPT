import discord
from discord.ext import commands
from utils.conversation_memory import with_message_history as memory_chatbot

class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ask(self, ctx: commands.Context, *, message: str):
        """Chat with Mistral"""
        response = memory_chatbot.invoke(
            {"input": message},
            config={"configurable": {"session_id": ctx.message.author.id}},
        )
        await ctx.send(response)
