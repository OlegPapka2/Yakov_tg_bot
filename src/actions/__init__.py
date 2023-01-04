from datetime import timedelta

from .ru_losses import ru_losses


def register_actions(updater):
    jq = updater.job_queue
    jq.run_repeating(ru_losses, interval=timedelta(days=1), first=1)
