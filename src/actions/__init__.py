from datetime import timedelta, time

import pytz

from .ru_losses import ru_losses
from .crypto import crypto
from .currency import currency
from .weather import weather


def register_actions(updater):
    jq = updater.job_queue
    timezone = pytz.timezone('Europe/Kyiv')

    jq.run_repeating(crypto, interval=timedelta(days=1), first=1)
    jq.run_repeating(currency, interval=timedelta(days=1), first=1)
    jq.run_daily(weather, time=time(hour=7, minute=30, second=0, tzinfo=timezone))
    jq.run_daily(ru_losses, time=time(hour=10, minute=0, second=0, tzinfo=timezone))
