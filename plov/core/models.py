import re

import django.conf
import django.contrib.contenttypes.fields
import django.contrib.contenttypes.models
import django.core.exceptions
import django.db.models
import slugify


class NormalizedNameModel(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name='Название',
        max_length=100,
        help_text='Уникальное название объекта (макс. 100 символов)',
    )
    slug = django.db.models.SlugField(
        verbose_name='URL-идентификатор',
        max_length=100,
        unique=True,
        help_text='Уникальная часть URL для этого объекта (макс. 100 символов)',
    )
    normalized_name = django.db.models.CharField(
        verbose_name='Нормализованное название',
        max_length=255,
        unique=True,
        editable=False,
        help_text='Автоматически генерируемая нормализованная версия названия',
    )

    class Meta:
        abstract = True
        indexes = [
            django.db.models.Index(fields=['normalized_name']),
        ]
        verbose_name = 'Объект с нормализованным именем'
        verbose_name_plural = 'Объекты с нормализованными именами'

    def get_normalized_name(self):
        remove_punctuation_regex = re.compile(r'[^-_\w\s]')
        no_punctuation_name = remove_punctuation_regex.sub('', str(self.name))
        return slugify.slugify(no_punctuation_name)

    def clean(self):
        normalized_name = self.get_normalized_name()
        if type(self).objects.exclude(id=self.id).filter(normalized_name=normalized_name).exists():
            raise django.core.exceptions.ValidationError('Объект с таким названием уже существует.')

    def save(self, *args, **kwargs):
        self.normalized_name = self.get_normalized_name()
        if not self.slug:
            self.slug = slugify.slugify(self.name)

        super().save(*args, **kwargs)


class UserContentInteraction(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=django.db.models.CASCADE,
        help_text='Пользователь, взаимодействующий с контентом',
    )
    content_type = django.db.models.ForeignKey(
        django.contrib.contenttypes.models.ContentType,
        verbose_name='Тип контента',
        on_delete=django.db.models.CASCADE,
        help_text='Тип контента, с которым происходит взаимодействие',
    )
    object_id = django.db.models.PositiveIntegerField(verbose_name='ID объекта', help_text='ID объекта контента')
    content_object = django.contrib.contenttypes.fields.GenericForeignKey(
        'content_type',
        'object_id',
    )
    created_at = django.db.models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='Дата и время создания взаимодействия',
    )

    class Meta:
        abstract = True
        indexes = [
            django.db.models.Index(fields=['content_type', 'object_id']),
        ]
        verbose_name = 'Взаимодействие пользователя с контентом'
        verbose_name_plural = 'Взаимодействия пользователей с контентом'


class Report(django.db.models.Model):
    reporter = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name='Автор жалобы',
        on_delete=django.db.models.CASCADE,
        help_text='Пользователь, отправивший жалобу',
    )

    reason = django.db.models.TextField(
        verbose_name='Причина жалобы',
        max_length=1000,
        blank=True,
        help_text='Подробное описание причины жалобы (макс. 1000 символов)',
    )

    created = django.db.models.DateTimeField(
        verbose_name='Дата создания жалобы',
        editable=False,
        auto_now_add=True,
        null=True,
        help_text='Дата и время подачи жалобы',
    )

    class Meta:
        abstract = True
        ordering = ['-created']
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
