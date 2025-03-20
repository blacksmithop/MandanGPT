from discord.ext import commands
from discord.ext.commands import Context
from utils import summarize_text, LangchainFailiure
from discord import Embed


class NLP(commands.Cog, name="nlp"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="summarize",
        description="Summarize text.",
    )
    async def summarize(self, context: Context, *, text: str) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
        """
        try:
            async with context.typing():
                summary = summarize_text(text=text)
                embed = Embed(description=summary, color=0xE02B2B)
                await context.send(embed=embed)
        except LangchainFailiure:
            embed = Embed(description="Failed to summarize text", color=0xE02B2B)
            await context.send(embed=embed)



async def setup(bot) -> None:
    await bot.add_cog(NLP(bot))
