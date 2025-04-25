import django.db.models

import core.models


class Vote(core.models.UserContentInteraction):
    class VoteChoices(django.db.models.TextChoices):
        UPVOTE = 'U', 'Лайк'
        DOWNVOTE = 'D', 'Дизлайк'

    vote_type = django.db.models.CharField(
        verbose_name='Тип голоса',
        choices=VoteChoices,
        max_length=1,
        help_text='Тип реакции пользователя (лайк или дизлайк)',
    )

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        default_related_name = 'votes'
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

    def __str__(self):
        return f'{self.user}: {self.get_vote_type_display()}'
