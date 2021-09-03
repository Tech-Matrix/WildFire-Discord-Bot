import os
from pathlib import Path
from typing import NamedTuple


class Client(NamedTuple):
    # token = os.environ.get("BOT_TOKEN")
    token = "ODgzMDIyOTM1MTY4Nzk0NjQ2.YTD5MQ.hqicEdG0Tu9jfJR_-We8XunIQu4"
    extensions = Path("bot", "exts").glob('**/*.py')


class Channels(NamedTuple):
    dev_logs = 883341513428455445
    dev_alerts = 883058563302428752
