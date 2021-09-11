import os
from contextlib import suppress
from pathlib import Path
from typing import NamedTuple


with suppress(ImportError):
    # No docker.
    from dotenv import load_dotenv
    load_dotenv()


class Client(NamedTuple):
    token = os.environ.get("BOT_TOKEN")
    extensions = Path("bot", "exts").glob('**/*.py')
    database_url = os.environ.get("DATABASE_URL")


class Channels(NamedTuple):
    dev_logs = 883341513428455445
    dev_alerts = 883058563302428752
    mod_alerts = 885232447086817312


class Roles(NamedTuple):
    mods = 885233543284928573