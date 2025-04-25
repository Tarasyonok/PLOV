import logging

import celery
import django.utils
import users.models

logger = logging.getLogger(__name__)


@celery.shared_task
def auto_unban_users():
    try:
        expired_bans = users.models.User.objects.filter(is_banned=True, ban_ends_at__lte=django.utils.timezone.now())
        count = expired_bans.count()

        expired_bans.update(is_banned=False, ban_reason='', banned_at=None, ban_ends_at=None)

        logger.info(f'Auto-unbanned {count} users')
        return f'Unbanned {count} users'

    except Exception as e:
        logger.error(f'Auto-unban failed: {str(e)}')
        raise
