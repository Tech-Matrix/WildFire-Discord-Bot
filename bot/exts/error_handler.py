import logging

import lightbulb
from lightbulb.errors import CheckFailure, NotEnoughArguments
from lightbulb.events import CommandErrorEvent

from bot.bot import Bot


logger = logging.getLogger(__name__)


class ErrorHandler(lightbulb.Plugin):

    @lightbulb.listener(CommandErrorEvent)
    async def on_command_error(self, event: CommandErrorEvent) -> None:
        """Error handler."""
        if isinstance(event.exception, CheckFailure):
            await event.context.respond("You do not have the permissions to run this command!")

        elif isinstance(event.exception, NotEnoughArguments):
            await event.context.respond("Not enough arguments!")

        else:
            raise event.exception


def load(bot: Bot) -> None:
    bot.add_plugin(ErrorHandler())
