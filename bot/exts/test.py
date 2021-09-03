from bot.bot import Bot

import lightbulb


class Ping(lightbulb.Plugin):

    @lightbulb.command(name="ping")
    async def ping(self, ctx: lightbulb.Context) -> None:
        """Responds with `Pong!`."""
        await ctx.respond("Pong!")


def load(bot: Bot) -> None:
    bot.add_plugin(Ping())
