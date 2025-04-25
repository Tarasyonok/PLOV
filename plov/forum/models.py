import django.conf
import django.db.models
import django.urls

import core.models


class Topic(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=django.db.models.CASCADE,
        help_text='Пользователь, создавший топик',
    )
    title = django.db.models.CharField(
        verbose_name='Заголовок',
        max_length=256,
        null=True,
        help_text='Название топика (макс. 256 символов)',
    )
    text = django.db.models.TextField(
        verbose_name='Текст топика',
        max_length=1000,
        help_text='Содержание топика (макс. 1000 символов)',
    )
    created = django.db.models.DateTimeField(
        verbose_name='Дата создания',
        editable=False,
        auto_now_add=True,
        null=True,
        help_text='Дата и время создания топика',
    )

    class Meta:
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'

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
        'forum.Topic',
        verbose_name='Топик',
        on_delete=django.db.models.CASCADE,
        help_text='Топик, к которому относится ответ',
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=django.db.models.CASCADE,
        help_text='Пользователь, оставивший ответ',
    )
    text = django.db.models.TextField(
        verbose_name='Текст ответа',
        max_length=1000,
        help_text='Содержание ответа (макс. 1000 символов)',
    )
    created = django.db.models.DateTimeField(
        verbose_name='Дата создания',
        editable=False,
        auto_now_add=True,
        null=True,
        help_text='Дата и время создания ответа',
    )
    upvotes: django.db.models.ManyToManyField = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Голоса "за"',
        blank=True,
        related_name='upvotes',
        help_text='Пользователи, проголосовавшие за ответ',
    )
    downvotes: django.db.models.ManyToManyField = django.db.models.ManyToManyField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Голоса "против"',
        blank=True,
        related_name='downvotes',
        help_text='Пользователи, проголосовавшие против ответа',
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.topic.title

    @property
    def upvotes_count(self):
        return Answer.objects.filter(user=self).count()


class TopicView(django.db.models.Model):
    topic = django.db.models.ForeignKey(
        'forum.Topic',
        verbose_name='Топик',
        on_delete=django.db.models.CASCADE,
        help_text='Просматриваемый топик',
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=django.db.models.CASCADE,
        help_text='Пользователь, просмотревший топик',
    )

    class Meta:
        verbose_name = 'Просмотр топика'
        verbose_name_plural = 'Просмотры топиков'

    def __str__(self):
        return self.topic.title


class TopicReport(core.models.Report):
    topic = django.db.models.ForeignKey(
        'forum.Topic',
        verbose_name='Топик',
        on_delete=django.db.models.CASCADE,
        help_text='Топик, на который поступила жалоба',
    )

    class Meta:
        verbose_name = 'Жалоба на топик'
        verbose_name_plural = 'Жалобы на топики'

    def __str__(self):
        return f'Жалоба на топик от {self.reporter}'


class AnswerReport(core.models.Report):
    answer = django.db.models.ForeignKey(
        'forum.Answer',
        verbose_name='Ответ',
        on_delete=django.db.models.CASCADE,
        help_text='Ответ, на который поступила жалоба',
    )

    class Meta:
        verbose_name = 'Жалоба на ответ'
        verbose_name_plural = 'Жалобы на ответы'

    def __str__(self):
        return f'Жалоба на ответ от {self.reporter}'
