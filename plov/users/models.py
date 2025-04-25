import django.conf
import django.contrib.auth.models
import django.core.validators
import django.db.models
import django.utils.deconstruct
import django.utils.timezone
import users.utils.validators

import stickers.models


class User(django.contrib.auth.models.AbstractUser):
    class Role(django.db.models.TextChoices):
        GUEST = 'guest', 'Гость'
        STUDENT = 'student', 'Ученик'
        MODERATOR = 'moderator', 'Модератор'
        MENTOR = 'mentor', 'Ментор'
        LEAD = 'lead', 'Лид'
        ADMIN = 'admin', 'Админ'

    role = django.db.models.CharField(max_length=20, choices=Role.choices, default=Role.GUEST, db_index=True)
    is_banned = django.db.models.BooleanField(default=False)
    ban_reason = django.db.models.TextField(blank=True, null=True, max_length=500)
    banned_at = django.db.models.DateTimeField(null=True, blank=True)
    ban_ends_at = django.db.models.DateTimeField(null=True, blank=True)

    email = django.db.models.EmailField(unique=True)
    lms_profile_id = django.db.models.CharField(max_length=100, null=True, blank=True, unique=True)
    telegram_username = django.db.models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True,
        validators=[django.core.validators.RegexValidator(r'^@[a-zA-Z0-9_]{5,32}$')],
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'User {self.username}'

    def is_moderator_or_higher(self):
        return self.role in [self.Role.MODERATOR, self.Role.MENTOR, self.Role.LEAD, self.Role.ADMIN]

    @property
    def is_currently_banned(self):
        return self.is_banned and (not self.ban_ends_at or django.utils.timezone.now() < self.ban_ends_at)

    def ban_user(self, duration_days=None, reason=''):
        self.is_banned = True
        self.ban_reason = reason
        now = django.utils.timezone.now()
        self.banned_at = now
        self.ban_ends_at = now + django.utils.timezone.timedelta(days=duration_days) if duration_days else None
        self.save(update_fields=['is_banned', 'ban_reason', 'banned_at', 'ban_ends_at'])

    def unban_user(self):
        self.is_banned = False
        self.ban_reason = ''
        self.banned_at = None
        self.ban_ends_at = None
        self.save(update_fields=['is_banned', 'ban_reason', 'banned_at', 'ban_ends_at'])


def avatar_upload_to(self, filename: str) -> str:
    return f'users/{self.user.username}/{filename}'


class UserProfile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name='profile',
    )
    avatar = django.db.models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        validators=[
            django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']),
        ],
    )
    bio = django.db.models.TextField(blank=True)
    reputation_points = django.db.models.IntegerField(default=0, db_index=True)
    birthday = django.db.models.DateField(
        blank=True,
        null=True,
        validators=[
            users.utils.validators.YearRangeValidator(2000, -10),
        ],
    )
    last_activity = django.db.models.DateTimeField(default=django.utils.timezone.now)
    featured_stickers = django.db.models.ManyToManyField(stickers.models.Sticker)

    def __str__(self):
        return f'Profile of {self.user.username}'


class UserCourse(django.db.models.Model):
    class SpecializationChoices(django.db.models.TextChoices):
        DJANGO = 'D', 'Веб-разработка на Django'
        ML = 'M', 'Машинное обучение'
        BIGDATA = 'B', 'Большие данные'
        GOLANG = 'G', 'Веб-разработка на Go'
        ANALYTICS = 'A', 'Анализ данных'

    class SeasonChoices(django.db.models.TextChoices):
        WINTER = 'W', 'Зима'
        SPRING = 'S', 'Весна'
        SUMMER = 'U', 'Лето'
        FALL = 'F', 'Осень'

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name='courses',
    )
    specialization = django.db.models.CharField(choices=SpecializationChoices, default=SpecializationChoices.DJANGO)
    rating = django.db.models.IntegerField(
        db_index=True,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(200),
        ],
    )
    flow_season = django.db.models.CharField(choices=SeasonChoices.choices)
    flow_year = django.db.models.IntegerField(
        validators=[
            users.utils.validators.YearRangeValidator(2000, +1),
        ],
    )
    is_graduated = django.db.models.BooleanField(default=False)

    class Meta:
        constraints = [
            django.db.models.UniqueConstraint(
                fields=['user', 'specialization'],
                name='unique_course_user_specialization',
                violation_error_message='User already has this course specialization',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.get_specialization_display()}'
