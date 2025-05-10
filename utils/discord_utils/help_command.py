from discord.ext.commands import Cog, Context, Command, HybridCommand
from typing import List, Optional, Union
from discord.app_commands import Cooldown
from .embed_creator import create_datetime_embed
from discord.ext.commands import Converter
from utils import HelpCmdArgs
from discord import Embed, Member, User, app_commands
import shlex
import inspect

class HelpCommandArgParser(Converter):
    async def convert(self, ctx, arguments):
        try:
            # Use shlex to handle quoted strings and spaces
            args = shlex.split(arguments.strip())
        except ValueError:
            # Fallback to simple split if shlex fails (e.g., unmatched quotes)
            args = arguments.strip().split()

        if not args:
            return HelpCmdArgs()

        if len(args) == 1:
            return HelpCmdArgs(cog_name=args[0])
        elif len(args) == 2:
            return HelpCmdArgs(cog_name=args[0], cmd_name=args[1], cog_or_cmd_name=args[0])
        else:
            return HelpCmdArgs(error="Invalid number of arguments. Use: [cog] or [cog] [command]")

def generate_man_page(
    cog_command_mapping: dict,
    user: Optional[Union[User, Member]] = None,
    args: Optional[HelpCmdArgs] = None,
):
    # Base embed setup
    help_embed = create_datetime_embed(
        user=user,
        title="🖥️ MandanGPT Help Manual",
        description="A comprehensive guide to available commands and modules."
    )

    # Handle parsing errors
    if getattr(args, 'error', None):
        help_embed.add_field(
            name="⚠️ Error",
            value=args.error,
            inline=False
        )
        return help_embed

    # Case 1: No arguments - show all cogs
    if not args or (not args.cog_name and not args.cmd_name):
        cog_names = list(cog_command_mapping.keys())
        help_embed.add_field(
            name="📚 Available Modules",
            value="\n".join(f"**{i+1}.** {name}" for i, name in enumerate(cog_names)) or "No modules available.",
            inline=False
        )
        help_embed.add_field(
            name="ℹ️ Usage",
            value="Use `!help [module]` to see commands in a module\nUse `!help [module] [command]` for command details",
            inline=False
        )
        return help_embed

    cog_name, cmd_name = args.cog_name, args.cmd_name
    ambiguous_name = args.cog_or_cmd_name

    # Resolve cog name
    if cog_name and cog_name in cog_command_mapping:
        pass
    elif ambiguous_name and ambiguous_name in cog_command_mapping:
        cog_name = ambiguous_name
        cmd_name = None
    else:
        help_embed.add_field(
            name="⚠️ Error",
            value=f"Could not find module '{cog_name or ambiguous_name}'. Use `!help` to see available modules.",
            inline=False
        )
        return help_embed

    # Case 2: Cog specified, no command - show all commands in cog
    cog_commands = cog_command_mapping[cog_name]
    if not cmd_name:
        help_embed.title = f"🖥️ MandanGPT Help - {cog_name}"
        command_list = "\n".join(f"**{name}**" for name in cog_commands.keys()) or "No commands available."
        help_embed.add_field(
            name="📜 Commands",
            value=command_list,
            inline=True
        )
        help_embed.add_field(
            name="ℹ️ Usage",
            value=f"Use `!help {cog_name} [command]` to see details for a specific command.",
            inline=False
        )
        return help_embed

    # Case 3: Cog and command specified - show command details
    if cmd_name in cog_commands:
        help_embed.title = f"🖥️ MandanGPT Help - {cog_name}::{cmd_name}"
        help_embed.add_field(
            name="📋 Command Details",
            value=cog_commands[cmd_name],
            inline=False
        )
        return help_embed
    else:
        help_embed.add_field(
            name="⚠️ Error",
            value=f"Command '{cmd_name}' not found in module '{cog_name}'. Use `!help {cog_name}` to see available commands.",
            inline=False
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

            # Get traditional and hybrid commands
            commands = cog.get_commands()
            self.walk_commands_and_generate_help_text(commands=commands, cog_name=cog_name)

            # Get app commands (slash commands)
            app_commands = cog.get_app_commands()
            self.walk_app_commands_and_generate_help_text(app_commands=app_commands, cog_name=cog_name)

    def walk_commands_and_generate_help_text(
        self, commands: List[Union[Command, HybridCommand]], cog_name: str
    ):
        for command in commands:
            command_name = command.name
            description = command.description or "No description available."
            help_text = command.help or "No additional help text."
            aliases = command.aliases
            params = command.clean_params
            enabled = command.enabled
            hidden = command.hidden
            is_greedy = not command.ignore_extra

            cooldown: Cooldown = command.cooldown
            cooldown_info = f"{cooldown.rate}/{cooldown.per}" if cooldown else "None"

            # Format parameters
            param_info = "\n".join(
                f"**{name}**: {param.annotation.__name__ if param.annotation != inspect.Parameter.empty else 'Any'}"
                for name, param in params.items()
            ) or "No parameters."

            command_help_text = (
                f"**Type**: Hybrid Command\n"
                f"**Description**: {description}\n"
                f"**Parameters**:\n{param_info}\n"
                f"**Greedy**: {is_greedy}\n"
                f"**Aliases**: {', '.join(aliases) if aliases else 'None'}\n"
                f"**Enabled**: {enabled}\n"
                f"**Hidden**: {hidden}\n"
                f"**Cooldown**: {cooldown_info}"
            )

            self.cog_commands[cog_name][command_name] = command_help_text

    def walk_app_commands_and_generate_help_text(
        self, app_commands: List[app_commands.Command], cog_name: str
    ):
        for command in app_commands:
            command_name = command.name
            description = command.description or "No description available."
            # App commands don't have a direct help attribute, so we'll use description
            help_text = description
            # App commands don't have aliases in the same way, but they can have autocomplete
            aliases = []  # You can extend this if you have custom alias logic for app commands
            enabled = True  # App commands are enabled by default
            hidden = False  # App commands don't have a hidden attribute by default
            is_greedy = False  # App commands don't support greedy parsing

            # Get cooldown information if it exists
            cooldown = getattr(command, 'cooldown', None)
            cooldown_info = f"{cooldown.rate}/{cooldown.per}" if cooldown else "None"

            # Format parameters for app commands
            param_info = "\n".join(
                f"**{param.name}**: {param.type.name if param.type else 'Any'}"
                for param in command.parameters
            ) or "No parameters."

            command_help_text = (
                f"**Type**: Slash Command\n"
                f"**Description**: {description}\n"
                f"**Help Text**:\n```{help_text}```\n"
                f"**Parameters**:\n{param_info}\n"
                f"**Greedy**: {is_greedy}\n"
                f"**Aliases**: {', '.join(aliases) if aliases else 'None'}\n"
                f"**Enabled**: {enabled}\n"
                f"**Hidden**: {hidden}\n"
                f"**Cooldown**: {cooldown_info}"
            )

            self.cog_commands[cog_name][command_name] = command_help_text