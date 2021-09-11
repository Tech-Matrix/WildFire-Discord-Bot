import logging
import re
import typing
from typing import Optional

import hikari
import lightbulb
from hikari.events import GuildMessageCreateEvent

from bot.bot import Bot
from bot.constants import Channels, Roles
from model import predict

logger = logging.getLogger(__name__)


class Filter(lightbulb.Plugin):

    def __init__(self, bot: Bot, *, name: Optional[str] = None) -> None:
        super().__init__(name=name)

        self.bot = bot

        # TODO DATABASE CACHE: Cache all the words to censor according to guild.
        self._filter_cache: typing.Dict[re.Pattern: str] = {}

    def compile_regex(self) -> None:
        ...

    def match_filter_patterns(self, content: str) -> Optional[typing.Tuple[re.Match, str]]:
        """Try to find matches between registered filter patterns with a message."""
        for pattern, pattern_identifier in self._filter_cache.items():
            if search := pattern.search(content):
                return search, pattern_identifier

    async def notify_mods(
            self, event: GuildMessageCreateEvent, matching_content: Optional[str], type_of_filter: str
    ) -> None:
        """Notify moderators when a message filter is triggered."""
        message_channel = self.bot.cache.get_guild_channel(event.message.channel_id)
        user = event.message.author

        channel = self.bot.cache.get_guild_channel(Channels.mod_alerts)

        description = (
            f"**Sent by {user.mention} in {message_channel.mention}\n"
            f"{'Filter matching content**:' if matching_content else ''}\n"
            f"**Full message:**\n{event.message.content}"
        )

        embed = hikari.Embed(
            title=f"**Filter triggered:** {type_of_filter}",
            description=description,
            colour=hikari.Color.of((255, 255, 255))
        )
        mods_role = self.bot.cache.get_role(Roles.mods)
        await channel.send(content=mods_role.mention, embed=embed)

        await event.message.delete()

    @lightbulb.group(name="filter", inherit_checks=True)
    async def filter_content(self, ctx: lightbulb.Context) -> None:
        """Filter messages using patterns(regex) or words."""
        await ctx.send_help(ctx.command)

    @filter_content.command(name="add")
    async def add_content_filter(self, ctx: lightbulb.Context, name: str, pattern: str):
        """Add message filter."""
        # Run regex validation
        self._filter_cache[re.compile(pattern)] = name

        await ctx.respond("Filter has been added!")
        
    @filter_content.command(name="list")
    async def list_content_filters(self, ctx: lightbulb.Context):
        pass

    @lightbulb.listener(GuildMessageCreateEvent)
    async def on_message(self, event):
        """Filter messages when sent."""
        if event.author.is_bot:
            return

        content = event.message.content

        if filter_match := self.match_filter_patterns(content):
            # notify mods
            match, pattern_identifier = filter_match

            matching_span = match.span()
            matching_content = content[matching_span[0]:matching_span[1]]

            await self.notify_mods(event, f"...{matching_content}...", pattern_identifier)

        elif predict(self.bot.vectorizer, content):
            await self.notify_mods(event, None, "Offensive message")

    async def plugin_check(self, ctx: lightbulb.Context):
        if Roles.mods in [role.id for role in ctx.member.get_roles()]:
            return True
        return False


def load(bot: Bot) -> None:
    bot.add_plugin(Filter(bot))
