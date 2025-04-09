import platform
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from utils import FeedbackForm, generate_man_page, HelpCommandArgParser
from typing import Optional


class General(commands.Cog, name="General"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(
        self, context: Context, *, args: Optional[HelpCommandArgParser] = None
    ) -> None:
        # is_owner = await self.bot.is_owner(context.author)
        cog_commands = self.bot.help_command_handler.cog_commands
        response = generate_man_page(
            user=self.bot.user, args=args, cog_command_mapping=cog_commands
        )
        await context.send(embed=response)

    @commands.hybrid_command(
        name="about",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0xBEBEFE,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="Krypton#7331", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here]({self.bot.config['invite_link']}).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @app_commands.command(
        name="feedback", description="Submit a feedback for the owners of the bot"
    )
    async def feedback(self, interaction: discord.Interaction) -> None:
        """
        Submit a feedback for the owners of the bot.

        :param context: The hybrid command context.
        """
        feedback_form = FeedbackForm()
        await interaction.response.send_modal(feedback_form)

        await feedback_form.wait()
        interaction = feedback_form.interaction
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Thank you for your feedback, the owners have been notified about it.",
                color=0xBEBEFE,
            )
        )

        app_owner = (await self.bot.application_info()).owner
        await app_owner.send(
            embed=discord.Embed(
                title="New Feedback",
                description=f"{interaction.user} (<@{interaction.user.id}>) has submitted a new feedback:\n```\n{feedback_form.answer}\n```",
                color=0xBEBEFE,
            )
        )

    # Dummy command to mess around with the ui kit
    # @app_commands.command(
    #     name="pagination",
    #     description="test pagination",
    # )
    # async def pagination(self, interaction: Interaction):
    #     async def get_page(page: int):
    #         emb = discord.Embed(title="The Users", description="")
    #         offset = (page - 1) * L
    #         for user in users[offset : offset + L]:
    #             emb.description += f"{user}\n"
    #         emb.set_author(name=f"Requested by {interaction.user}")
    #         n = Pagination.compute_total_pages(len(users), L)
    #         emb.set_footer(text=f"Page {page} from {n}")
    #         return emb, n

    #     await Pagination(interaction, get_page).navigate()


async def setup(bot) -> None:
    await bot.add_cog(General(bot))
