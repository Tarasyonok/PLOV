# flake8: noqa: E800
import django.contrib.admin

import forum.models

django.contrib.admin.site.register(forum.models.Topic)
django.contrib.admin.site.register(forum.models.Answer)
django.contrib.admin.site.register(forum.models.TopicView)


@django.contrib.admin.register(forum.models.TopicReport)
class TopicReportAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'reporter',
        'reason',
        'topic',
    )
    readonly_fields = (
        'reporter',
        'reason',
        'topic',
    )
    list_display_links = (
        'reporter',
        'topic',
    )


@django.contrib.admin.register(forum.models.AnswerReport)
class AnswerReportAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        'reporter',
        'reason',
        'answer',
    )
    readonly_fields = (
        'reporter',
        'reason',
        'answer',
    )
    list_display_links = (
        'reporter',
        'answer',
    )
