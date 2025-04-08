import django.conf
import django.db.models

import users.models


class Review(django.db.models.Model):
    class RatingChoices(django.db.models.IntegerChoices):
        HATE = 1, 'Ужасно'
        DISLIKE = 2, 'Плохо'
        OK = 3, 'Нормально'
        LIKE = 4, 'Хорошо'
        LOVE = 5, 'Отлично'

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        unique=True,
    )
    specialization = django.db.models.CharField(
        choices=users.models.UserCourse.SpecializationChoices,
        default=users.models.UserCourse.SpecializationChoices.DJANGO,
    )
    rating = django.db.models.PositiveSmallIntegerField(choices=RatingChoices)
    content = django.db.models.TextField()
    created_at = django.db.models.DateTimeField(auto_now_add=True)
    updated_at = django.db.models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return f"{self.rating}/5 review by {self.user or 'Anonymous'}"
