import logging

import lightbulb
from lightbulb.errors import CheckFailure
from lightbulb.events import CommandErrorEvent

from bot.bot import Bot


logger = logging.getLogger(__name__)


class ErrorHandler(lightbulb.Plugin):

    @lightbulb.listener(CommandErrorEvent)
    async def on_command_error(self, event: CommandErrorEvent) -> None:
        """Error handler."""
        if isinstance(event.exception, CheckFailure):
            await event.context.respond("You do not have the permissions to run this command!")
        else:
            raise event.exception


def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler())
