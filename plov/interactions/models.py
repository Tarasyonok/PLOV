import django.db.models

import core.models


class Comment(core.models.UserContentInteraction):
    content = django.db.models.TextField()
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
    )
    is_edited = django.db.models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.is_edited = True

        super().save(*args, **kwargs)

    class Meta:
        default_related_name = 'comments'
        indexes = [
            django.db.models.Index(fields=['created_at'], name='idx_comment_created_at'),
        ]

    def __str__(self):
        return f'Comment by {self.user.username}'


class Vote(core.models.UserContentInteraction):
    class VoteChoices(django.db.models.TextChoices):
        UPVOTE = 'U', 'Лайк'
        DOWNVOTE = 'D', 'Дизлайк'

    specialization = django.db.models.CharField(
        choices=VoteChoices,
    )

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        default_related_name = 'likes'

    def __str__(self):
        return f'{self.user.username} likes {self.content_object}'
