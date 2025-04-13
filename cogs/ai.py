from discord.ext import commands
from discord.ext.commands import Context
from utils import SummaryTypeView  # LangchainFailiure
from typing import Optional
from discord import app_commands, Embed, Interaction


class ArtificalIntelligence(commands.Cog, name="Artificial Intelligence"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="summarize", description="Summarize text with customizable parameters"
    )
    async def summarize(self, interaction: Interaction):
        """Command to start the summarization process"""
        view = SummaryTypeView()
        await interaction.response.send_message(
            "🔍 Choose a model for summarization:", view=view, ephemeral=False
        )


async def setup(bot) -> None:
    await bot.add_cog(ArtificalIntelligence(bot))
