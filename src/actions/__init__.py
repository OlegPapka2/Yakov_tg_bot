from datetime import timedelta

from .ru_losses import ru_losses
from .crypto import crypto
from .currency import currency
from .weather import weather


def register_actions(updater):
    jq = updater.job_queue
    jq.run_repeating(ru_losses, interval=timedelta(days=1), first=1)
    jq.run_repeating(crypto, interval=timedelta(days=1), first=1)
    jq.run_repeating(currency, interval=timedelta(days=1), first=1)
    jq.run_repeating(weather, interval=timedelta(days=1), first=1)
