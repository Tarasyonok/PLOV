import django.conf
import django.contrib.contenttypes.fields
import django.contrib.contenttypes.models
import django.db.models

import interactions.models
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
        verbose_name='Пользователь',
        on_delete=django.db.models.SET_NULL,
        null=True,
        blank=True,
        help_text='Автор отзыва (может быть анонимным)',
    )
    specialization = django.db.models.CharField(
        verbose_name='Специализация',
        choices=users.models.UserCourse.SpecializationChoices,
        default=users.models.UserCourse.SpecializationChoices.DJANGO,
        max_length=50,
        help_text='Направление обучения, к которому относится отзыв',
    )
    rating = django.db.models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        choices=RatingChoices.choices,
        help_text='Оценка курса от 1 (ужасно) до 5 (отлично)',
    )
    content = django.db.models.TextField(
        verbose_name='Текст отзыва',
        help_text='Содержание отзыва (максимальная длина не ограничена)',
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='Дата и время создания отзыва',
    )
    updated_at = django.db.models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True,
        db_index=True,
        help_text='Дата и время последнего обновления отзыва',
    )

    votes = django.contrib.contenttypes.fields.GenericRelation(
        'interactions.Vote',
        verbose_name='Голоса',
        related_query_name='review',
        help_text='Голоса за/против этого отзыва',
    )

    @property
    def upvotes_count(self):
        return self.votes.filter(vote_type=interactions.models.Vote.VoteChoices.UPVOTE).count()

    @property
    def downvotes_count(self):
        return self.votes.filter(vote_type=interactions.models.Vote.VoteChoices.DOWNVOTE).count()

    def get_user_vote(self, user):
        if not user.is_authenticated:
            return None

        content_type = django.contrib.contenttypes.models.ContentType.objects.get_for_model(self)
        vote = interactions.models.Vote.objects.filter(user=user, content_type=content_type, object_id=self.id).first()
        return vote.vote_type if vote else None

    class Meta:
        constraints = [
            django.db.models.UniqueConstraint(
                fields=['user', 'specialization'],
                name='unique_review_user_specialization',
                violation_error_message='Этот пользователь уже оставлял отзыв на этот курс',
            ),
        ]
        ordering = ['-created_at']
        indexes = [
            django.db.models.Index(fields=['specialization']),
            django.db.models.Index(fields=['rating']),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв {self.rating}/5 от {self.user or 'Анонима'}"
