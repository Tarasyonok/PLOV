import django.conf
import django.db.models


class Report(django.db.models.Model):
    reporter = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name="жалующийся",
        on_delete=django.db.models.CASCADE,
    )

    reason = django.db.models.TextField(
        max_length=1000,
        verbose_name="жалоба",
        blank=True,
    )

    created = django.db.models.DateTimeField(
        verbose_name="дата поступления жалобы",
        editable=False,
        auto_now_add=True,
        null=True,
        help_text="Дата поступления жалобы.",
    )

    class Meta:
        abstract = True
