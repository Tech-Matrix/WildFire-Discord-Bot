from bot.bot import Bot

from bot.constants import Client

bot = Bot.create(
    token=Client.token,
    prefix=".",  # Need to change to use a func.
)

bot.run()
