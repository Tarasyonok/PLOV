import re

import django.conf
import django.contrib.contenttypes.fields
import django.contrib.contenttypes.models
import django.core.exceptions
import django.db.models
import slugify


class NormalizedNameModel(django.db.models.Model):
    name = django.db.models.CharField(max_length=100)
    slug = django.db.models.SlugField(max_length=100, unique=True)
    normalized_name = django.db.models.CharField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True
        indexes = [
            django.db.models.Index(fields=['normalized_name']),
        ]

    def get_normalized_name(self):
        remove_punctuation_regex = re.compile(r'[^-_\w\s]')
        no_punctuation_name = remove_punctuation_regex.sub('', str(self.name))
        return slugify.slugify(no_punctuation_name)

    def clean(self):
        if len(str(self.emoji)) != 1:
            raise django.core.exceptions.ValidationError("Emoji must be a single character.")

        normalized_name = self.get_normalized_name()
        if type(self).objects.exclude(id=self.id).filter(normalized_name=normalized_name).exists():
            raise django.core.exceptions.ValidationError("Object with similar name already exists.")

    def save(self, *args, **kwargs):
        self.normalized_name = self.get_normalized_name()
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        super().save(*args, **kwargs)


class UserContentInteraction(django.db.models.Model):
    user = django.db.models.ForeignKey(
        to=django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
    )
    content_type = django.db.models.ForeignKey(
        django.contrib.contenttypes.models.ContentType,
        on_delete=django.db.models.CASCADE,
    )
    object_id = django.db.models.PositiveIntegerField()
    content_object = django.contrib.contenttypes.fields.GenericForeignKey(
        'content_type',
        'object_id',
    )
    created_at = django.db.models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
