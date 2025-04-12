import django.forms
import forum.models


class TopicForm(django.forms.ModelForm):
    title = django.forms.CharField(
        label="",
        widget=django.forms.TextInput(
            attrs={
                "class": "form-control form-control-style-3",
                "placeholder": "Заголовок",
            }
        ),
    )

    text = django.forms.CharField(
        label="",
        widget=django.forms.Textarea(
            attrs={
                "class": "form-control form-control-style-3",
                "placeholder": "Текст...",
                "rows": "8",
                "cols": "80",
            }
        ),
    )

    class Meta:
        model = forum.models.Topic
        fields = (
            "title",
            "text",
        )


class AnswerForm(django.forms.ModelForm):
    text = django.forms.CharField(
        label="",
        widget=django.forms.Textarea(
            attrs={
                "class": "form-control form-control-style-3",
                "placeholder": "Текст...",
                "rows": "8",
                "cols": "50",
            }
        ),
    )

    class Meta:
        model = forum.models.Answer
        fields = [
            "text",
        ]


class TopicReportForm(django.forms.ModelForm):
    reason = django.forms.CharField(
        label="",
        widget=django.forms.Textarea(
            attrs={
                "class": "form-control form-control-style-3",
                "placeholder": "Ваша жалоба...",
                "rows": "8",
                "cols": "50",
            }
        ),
    )

    class Meta:
        model = forum.models.TopicReport
        fields = [
            "reason",
        ]


class AnswerReportForm(django.forms.ModelForm):
    reason = django.forms.CharField(
        label="",
        widget=django.forms.Textarea(
            attrs={
                "class": "form-control form-control-style-3",
                "placeholder": "Ваша жалоба...",
                "rows": "8",
                "cols": "50",
            }
        ),
    )

    class Meta:
        model = forum.models.AnswerReport
        fields = [
            "reason",
        ]
