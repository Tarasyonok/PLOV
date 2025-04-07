import logging

from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import User, UserCourse, UserProfile
from users.utils.lms import LMSClient

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def check_lms_profile_change(sender, instance, **kwargs):
    if not hasattr(instance, '_lms_sync_data'):
        instance._lms_sync_data = {'needs_sync': False, 'lms_data': None}

    if not instance.pk and instance.lms_profile_id:
        instance._lms_sync_data['needs_sync'] = True

    elif instance.pk:
        try:
            current = User.objects.get(pk=instance.pk)
            if instance.lms_profile_id != current.lms_profile_id:
                instance._lms_sync_data['needs_sync'] = True
        except User.DoesNotExist:
            pass

    if instance._lms_sync_data['needs_sync'] and instance.lms_profile_id:
        try:
            client = LMSClient()
            lms_data = client.get_profile(instance.lms_profile_id)
            instance._lms_sync_data['lms_data'] = lms_data
        except Exception:
            instance._lms_sync_data['needs_sync'] = False


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def handle_lms_courses(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    if not getattr(instance, '_lms_sync_data', {}).get('needs_sync'):
        return

    lms_data = instance._lms_sync_data.get('lms_data')
    if not lms_data:
        return

    def _update_user_profile():
        try:
            profile_data = lms_data['profile']
            User.objects.filter(pk=instance.pk).update(
                first_name=profile_data['firstName'],
                last_name=profile_data['lastName'],
            )
            UserCourse.objects.filter(user=instance).delete()
            courses_data = lms_data['coursesSummary']['student'] or []
            for course in courses_data:
                specialization = 'D'
                flow_season = 'S'
                flow_year = timezone.now().year
                is_graduated = True
                UserCourse.objects.create(
                    user=instance,
                    specialization=specialization,
                    rating=course.get('rating', 0),
                    flow_season=flow_season,
                    flow_year=flow_year,
                    is_graduated=is_graduated,
                )

        except Exception as e:
            logger.info(f'Failed connect LMS Profile, exception: {e}')

    transaction.on_commit(_update_user_profile)
