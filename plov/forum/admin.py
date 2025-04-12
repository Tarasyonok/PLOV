import django.contrib.admin
import forum.models

django.contrib.admin.site.register(forum.models.Topic)
django.contrib.admin.site.register(forum.models.Answer)
django.contrib.admin.site.register(forum.models.TopicView)
# django.contrib.admin.site.register(forum.models.TopicReport)
# django.contrib.admin.site.register(forum.models.AnswerReport)


@django.contrib.admin.register(forum.models.TopicReport)
class TopicReportAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        forum.models.TopicReport.reporter.field.name,
        forum.models.TopicReport.reason.field.name,
        forum.models.TopicReport.topic.field.name,
    )

    readonly_fields = (
        forum.models.TopicReport.reporter.field.name,
        forum.models.TopicReport.reason.field.name,
        forum.models.TopicReport.topic.field.name,
    )
    list_display_links = (
        forum.models.TopicReport.reporter.field.name,
        forum.models.TopicReport.topic.field.name,
    )


@django.contrib.admin.register(forum.models.AnswerReport)
class AnswerReportAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        forum.models.AnswerReport.reporter.field.name,
        forum.models.AnswerReport.reason.field.name,
        forum.models.AnswerReport.answer.field.name,
    )

    readonly_fields = (
        forum.models.AnswerReport.reporter.field.name,
        forum.models.AnswerReport.reason.field.name,
        forum.models.AnswerReport.answer.field.name,
    )
    list_display_links = (
        forum.models.AnswerReport.reporter.field.name,
        forum.models.AnswerReport.answer.field.name,
    )
