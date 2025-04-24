import django.conf
import django.db.models
import django.urls

import core.models


class Topic(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        on_delete=django.db.models.CASCADE,
    )
    title = django.db.models.CharField(
        max_length=256,
        null=True,
    )
    text = django.db.models.TextField(
        max_length=1000,
    )
    created = django.db.models.DateTimeField(
        verbose_name='дата создания',
        editable=False,
        auto_now_add=True,
        null=True,
        help_text='Дата создания.',
    )

    class Meta:
        verbose_name = 'топик'
        verbose_name_plural = 'топики'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return django.urls.reverse(
            'forum:topic-detail',
            kwargs={'pk': self.pk},
        )

    @property
    def answer_count(self):
        return Answer.objects.filter(topic=self).count()

    @property
    def topic_view_count(self):
        return TopicView.objects.filter(topic=self).count()


class Answer(django.db.models.Model):
    topic = django.db.models.ForeignKey(
        Topic,
        verbose_name='топик',
        on_delete=django.db.models.CASCADE,
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        on_delete=django.db.models.CASCADE,
    )
    text = django.db.models.TextField(max_length=1000)
    created = django.db.models.DateTimeField(
        verbose_name='дата создания',
        editable=False,
        auto_now_add=True,
        null=True,
        help_text='Дата создания.',
    )
    upvotes = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='голоса: "да"',
        blank=True,
        related_name='upvotes',
    )
    downvotes = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='голоса: "нет"',
        blank=True,
        related_name='downvotes',
    )

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return self.topic.title

    @property
    def upvotes_count(self):
        return Answer.objects.filter(user=self).count()


class TopicView(django.db.models.Model):
    topic = django.db.models.ForeignKey(
        Topic,
        verbose_name='топик',
        on_delete=django.db.models.CASCADE,
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'просмотр топика'
        verbose_name_plural = 'просмотр топиков'

    def __str__(self):
        return self.topic.title


class TopicReport(core.models.Report):
    topic = django.db.models.ForeignKey(
        Topic,
        verbose_name='топик',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'жалоба на топик'
        verbose_name_plural = 'жалобы на топики'

    def __str__(self):
        return f'Жалоба на топик от {self.reporter}'


class AnswerReport(core.models.Report):
    answer = django.db.models.ForeignKey(
        Answer,
        verbose_name='ответ',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'жалоба на ответ'
        verbose_name_plural = 'жалобы на ответы'

    def __str__(self):
        return f'Жалоба на ответ от {self.reporter}'
