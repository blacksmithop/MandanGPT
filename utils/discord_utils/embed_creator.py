from discord import Embed, User
from datetime import datetime
from discord.member import Member
from typing import Optional, Union
from utils import bot_config
from .color import get_random_hex_color

def create_datetime_embed(title: str, description: Optional[str] = None, color: hex = get_random_hex_color(), user: Optional[Union[User, Member]] = None):
    embed = Embed(
        url=bot_config["github_repo_url"],
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now(),
    )
    if user:
        embed.set_author(
            name=user,
            icon_url=user.avatar.url,
        )
    return embed