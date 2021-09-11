import asyncio
import logging
import re
import typing
from collections import defaultdict
from typing import Optional, Union

import asyncpg
import hikari
import lightbulb
from hikari.events import GuildMessageCreateEvent

from bot.bot import Bot
from bot.constants import Channels, Roles
from model import predict
from postgres.utils import db_execute, db_fetch

logger = logging.getLogger(__name__)


class Filter(lightbulb.Plugin):

    def __init__(self, bot: Bot, *, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.bot = bot

        # TODO DATABASE CACHE: Cache all the words to censor according to guild.
        self._filter_cache: typing.Dict[re.Pattern: str] = defaultdict(dict)

        self.bot.loop.create_task(self._cache_patterns())

    async def _cache_patterns(self) -> None:
        """Cache all filter patterns."""
        results: [asyncpg.Record] = await db_fetch(
            self.bot.db_conn,
            "SELECT * FROM filter"
        )
        for result in results:
            re_compiled = re.compile(result["filter_pattern"])
            self._filter_cache[result["server_id"]][re_compiled] = [result["filter_identifier"]]

    def match_filter_patterns(self, content: str, guild_id: int) -> Optional[typing.Tuple[re.Match, str]]:
        """Try to find matches between registered filter patterns with a message."""
        for pattern, pattern_identifier in self._filter_cache[guild_id].items():
            if search := pattern.search(content):
                return search, pattern_identifier

    async def notify_mods(
            self,
            event: GuildMessageCreateEvent,
            matching_content: Optional[str],
            type_of_filter: str,
            footer: Optional[str] = None
    ) -> None:
        """Notify moderators when a message filter is triggered."""
        message_channel = self.bot.cache.get_guild_channel(event.message.channel_id)
        user = event.message.author

        channel = self.bot.cache.get_guild_channel(Channels.mod_alerts)

        description = (
            f"**Sent by {user.mention} in {message_channel.mention}**\n"
            f"{'**Filter matching content**:' if matching_content else ''}{matching_content}\n"
            f"**Full message:**\n{event.message.content}"
        )

        embed = hikari.Embed(
            title=f"**Filter triggered:** {type_of_filter}",
            description=description,
            colour=hikari.Color.of((255, 255, 255))
        )
        mods_role = self.bot.cache.get_role(Roles.mods)
        embed.set_footer(text=footer)
        await channel.send(content=mods_role.mention, embed=embed)

        await event.message.delete()

    @lightbulb.group(name="filter", inherit_checks=True)
    async def filter_content(self, ctx: lightbulb.Context) -> None:
        """Filter messages using patterns(regex) or words."""
        await ctx.send_help(ctx.command)

    @filter_content.command(name="add")
    async def add_content_filter(self, ctx: lightbulb.Context, name: str, pattern: str):
        """Add message filter."""
        # Run regex validation - after ib
        await db_execute(
            self.bot.db_conn,
            "INSERT INTO filter VALUES($1, $2, $3)",
            ctx.guild_id,
            name,
            pattern
        )

        self._filter_cache[ctx.guild_id][re.compile(pattern)] = re.compile(name)

        await ctx.respond("Filter has been added!")

    @filter_content.command(name="delete")
    async def delete_content_filter(self, ctx: lightbulb.Context, pattern: str) -> None:
        """Delete message filter."""
        # Run regex validation - after ib
        if not re.compile(pattern) in self._filter_cache[ctx.guild_id]:
            await ctx.respond("No such filter.")
            return

        await db_execute(
            self.bot.db_conn,
            "DELETE FROM filter WHERE server_id=$1 and filter_pattern=$2",
            ctx.guild_id,
            pattern
        )

        del self._filter_cache[ctx.guild_id][re.compile(pattern)]

        await ctx.respond("Filter has been deleted!")
        
    @filter_content.command(name="list")
    async def list_content_filters(self, ctx: lightbulb.Context):
        """List all filters."""
        results: [asyncpg.Record] = await db_fetch(
            self.bot.db_conn,
            "SELECT * FROM filter WHERE server_id=$1",
            ctx.guild_id,
        )
        message = "```Filters: Identifier - pattern\n"
        for i, result in enumerate(results, start=1):
            message += f"{i}. {result['filter_identifier']} - `{result['filter_pattern']}`\n"

        message += "```"
        await ctx.respond(message)

    @lightbulb.listener(GuildMessageCreateEvent)
    async def on_message(self, event: GuildMessageCreateEvent):
        """Filter messages when sent."""
        if event.author.is_bot:
            return

        if await self.plugin_check(event):
            return

        content = event.message.content

        if filter_match := self.match_filter_patterns(content, event.guild_id):
            # notify mods
            match, pattern_identifier = filter_match

            matching_span = match.span()
            matching_content = content[matching_span[0]:matching_span[1]]

            await self.notify_mods(event, f"...{matching_content}...", pattern_identifier)
        elif predict(self.bot.vectorizer, content):
            result: [asyncpg.Record] = await db_fetch(
                self.bot.db_conn,
                "SELECT * FROM offences WHERE server_id=$1 and user_id=$2",
                event.message.guild_id,
                event.message.author.id
            )
            if not result:
                await db_execute(
                    self.bot.db_conn,
                    "INSERT INTO offences VALUES ($1, $2, $3)",
                    event.message.guild_id,
                    event.message.author.id,
                    1
                )
                footer = f"Number of offences: {1}"
            else:
                await db_execute(
                    self.bot.db_conn,
                    "UPDATE offences SET num_of_offences=num_of_offences+1 WHERE server_id=$1 and user_id=$2",
                    event.message.guild_id,
                    event.message.author.id,
                )
                footer = f"Number of offences: {result[0]['num_of_offences']}"
            await self.notify_mods(event, None, "Offensive message", footer)

    async def plugin_check(self, ctx: Union[lightbulb.Context, GuildMessageCreateEvent]):
        """Return True for server moderator."""
        if Roles.mods in [role.id for role in ctx.member.get_roles()]:
            return True
        return False


def load(bot: Bot) -> None:
    bot.add_plugin(Filter(bot))
