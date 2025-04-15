import django.conf
import django.contrib.contenttypes.fields
import django.db.models
import interactions.models
from django.contrib.contenttypes.models import ContentType

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

    votes = django.contrib.contenttypes.fields.GenericRelation('interactions.Vote', related_query_name='review')

    @property
    def upvotes_count(self):
        return self.votes.filter(vote_type=interactions.models.Vote.VoteChoices.UPVOTE).count()

    @property
    def downvotes_count(self):
        return self.votes.filter(vote_type=interactions.models.Vote.VoteChoices.DOWNVOTE).count()

    def get_user_vote(self, user):
        if not user.is_authenticated:
            return None
        content_type = ContentType.objects.get_for_model(self)
        vote = interactions.models.Vote.objects.filter(
            user=user,
            content_type=content_type,
            object_id=self.id
        ).first()
        return vote.vote_type if vote else None

    def __str__(self):
        return f"{self.rating}/5 review by {self.user or 'Anonymous'}"
