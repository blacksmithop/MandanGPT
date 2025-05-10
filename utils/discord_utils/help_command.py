from discord.ext.commands import Cog, Context, Command, HybridCommand
from typing import List, Optional, Union
from discord.app_commands import Cooldown
from .embed_creator import create_datetime_embed
from discord.ext.commands import Converter
from utils import HelpCmdArgs
from discord import Embed, Member, User


class HelpCommandArgParser(Converter):
    async def convert(self, ctx, arguments):
        args = arguments.split(" ")
        match len(args):
            case 1:
                cmds = HelpCmdArgs(cog_name=arguments)
            case 2:
                cmds = HelpCmdArgs(
                    cog_name=args[0], cmd_name=args[1], cog_or_cmd_name=arguments
                )
            case _:
                cmds = HelpCmdArgs()
        return cmds


def generate_man_page(
    cog_command_mapping: dict,
    user: Optional[Union[User, Member]] = None,
    args: Optional[HelpCmdArgs] = None,
):
    if not args:
        cog_names = list(cog_command_mapping.keys())

        help_embed = create_datetime_embed(user=user, title="MandanGPT")

        module_info = ""
        for i, module_name in enumerate(cog_names):
            module_info += f"{i+1}. {module_name}\n"

        help_embed.add_field(name="Modules", value=module_info)
        return help_embed

    help_embed = create_datetime_embed(
        user=user, title="MandanGPT", description="Help Command"
    )
    cog_name, cmd_name = args.cog_name, args.cmd_name
    ambiguous_name = args.cog_or_cmd_name

    if cog_name and cog_name in cog_command_mapping.keys():
        ...
    elif ambiguous_name and ambiguous_name in cog_command_mapping.keys():
        cog_name = ambiguous_name
        cmd_name = None

    try:
        cog_commands = cog_command_mapping[cog_name]
        if not cmd_name:
            for command_name, help_text in cog_commands.items():
                help_embed.add_field(name=command_name, value=help_text, inline=False)
            return help_embed
        else:
            for command_name, help_text in cog_commands.items():
                if cmd_name == command_name:
                    help_embed.add_field(
                        name=command_name, value=help_text, inline=False
                    )
                return help_embed
    except KeyError:
        help_embed.add_field(
            name="Error", value=f"Could not find a Cog/Command named {cog_name}"
        )
        return help_embed


class HelpCommand:
    def __init__(self, prefix: str):
        self.cog_commands = {}
        self.prefix = prefix

    def walk_cogs_and_generate_help_text(self, cogs: List[Cog]):
        for _, cog in cogs.items():
            cog: Cog
            cog_name = cog.qualified_name
            if cog_name == "Admin":
                continue
            self.cog_commands[cog_name] = {}

            _cog_module_name = cog.__class__.__module__
            cog_file_name = _cog_module_name.split(".")[-1]

            commands = cog.get_commands()
            self.walk_commands_and_generate_help_text(
                commands=commands, cog_name=cog_name
            )

    def walk_commands_and_generate_help_text(
        self, commands: List[Union[Command, HybridCommand]], cog_name: str
    ):
        for command in commands:
            command_name = command.name
            description = command.description
            help_text = command.help
            module = command.module
            # qualified_name = command.qualified_name
            aliases = command.aliases
            # usage = command.usage

            # https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=parameter#parameter
            params = command.clean_params
            enabled = command.enabled
            hidden = command.hidden
            is_greedy = not command.ignore_extra

            cooldown: Cooldown = command.cooldown
            if cooldown:
                rate = cooldown.rate
                per = cooldown.per
                cooldown_info = f"{rate}/{per}"
            else:
                rate, per = None, None

            command_help_text = f"""\n{f'```{help_text}```'if help_text else ''}\n**Greedy**: {is_greedy}\n**Aliases**: {','.join(aliases) if cooldown else None}\n**Enabled**: {enabled}\n**Hidden**: {hidden}\n**Cooldown**: {cooldown_info if cooldown else None}"""

            self.cog_commands[cog_name][command_name] = command_help_text
