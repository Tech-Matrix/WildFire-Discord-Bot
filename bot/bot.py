import logging
import os
from pathlib import Path
from typing import Callable, Iterable, Union

import hikari
import lightbulb

from bot.constants import Channels, Client


logger = logging.getLogger(__name__)  # Required additional setup.


class Bot(lightbulb.Bot):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.dev_logs: hikari.GuildTextChannel = ...

    @classmethod
    def create(cls, token: str, *, prefix: Union[Callable, Iterable, str], **kwargs) -> "Bot":
        return cls(
            token=token,
            prefix=prefix,
            intents=hikari.Intents.ALL,
            insensitive_commands=True,
            **kwargs,
        )

    def run(self, **kwargs) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)

        super().run(
            activity=hikari.Activity(
                name=f"IceBreaker",
                type=hikari.ActivityType.PLAYING,
            ),
            **kwargs
        )

    async def on_starting(self, _event: hikari.StartingEvent) -> None:
        """Load extensions when bot is starting."""
        for ext in Client.extensions:
            self.load_extension(str(ext).replace(os.sep, ".")[:-3])

    async def on_started(self, _event: hikari.StartedEvent) -> None:
        """Notify dev-logs."""
        self.dev_logs = await self.rest.fetch_channel(Channels.dev_logs)
        await self.dev_logs.send(f"Bot online !")

        logging.info("Bot is ready.")

    async def on_stopping(self, _event: hikari.StoppingEvent) -> None:
        """Disconnect DB."""
        pass
