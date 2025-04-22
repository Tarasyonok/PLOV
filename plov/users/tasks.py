from celery import shared_task
from django.utils import timezone
from .models import User
import logging

logger = logging.getLogger(__name__)


@shared_task
def auto_unban_users():
    try:
        expired_bans = User.objects.filter(
            is_banned=True,
            ban_ends_at__lte=timezone.now()
        )
        count = expired_bans.count()

        expired_bans.update(
            is_banned=False,
            ban_reason="",
            banned_at=None,
            ban_ends_at=None
        )

        logger.info(f"Auto-unbanned {count} users")
        return f"Unbanned {count} users"

    except Exception as e:
        logger.error(f"Auto-unban failed: {str(e)}")
        raise
