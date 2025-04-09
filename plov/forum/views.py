import django.contrib.auth.decorators
import django.http
import django.shortcuts
import django.urls
import forum.forms
import forum.models


def topic_list(request):
    topics = forum.models.Topic.objects.all()
    latest_topics = forum.models.Topic.objects.order_by("-created")[0:5]
    context = {"topics": topics, "latest_topics": latest_topics}
    return django.shortcuts.render(request, "forum/topic_list.html", context)


@django.contrib.auth.decorators.login_required(login_url="/login/")
def topicPost(request):
    form = forum.forms.TopicForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            title = request.POST.get("title")
            text = request.POST.get("text")
            topic = forum.models.Topic.objects.create(
                title=title,
                user=request.user,
                text=text,
            )
            topic.save()
            return django.shortcuts.redirect("homepage:homepage")
    else:
        form = forum.forms.TopicForm()

    return django.shortcuts.render(
        request,
        "forum/topic_post.html",
        {"form": form},
    )


@django.contrib.auth.decorators.login_required(login_url="/login/")
def topicDetail(request, pk):
    post_topic = django.shortcuts.get_object_or_404(forum.models.Topic, pk=pk)
    if request.user.is_authenticated:
        forum.models.TopicView.objects.get_or_create(
            user=request.user,
            topic=post_topic,
        )

    answers = forum.models.Answer.objects.filter(topic=post_topic)
    answer_form = forum.forms.AnswerForm(request.POST or None)
    if request.method == "POST":
        if answer_form.is_valid():
            text = request.POST.get("text")
            ans = forum.models.Answer.objects.create(
                topic=post_topic,
                user=request.user,
                text=text,
            )
            ans.save()
            return django.http.HttpResponseRedirect(
                post_topic.get_absolute_url(),
            )
    else:
        answer_form = forum.forms.AnswerForm()

    context = {
        "topic": post_topic,
        "answers": answers,
        "answer_form": answer_form,
    }

    return django.shortcuts.render(request, "forum/topic_detail.html", context)


def upvote(request):
    answer = django.shortcuts.get_object_or_404(
        forum.models.Answer,
        id=request.POST.get("answer_id"),
    )

    if answer.upvotes.filter(id=request.user.id).exists():
        answer.upvotes.remove(request.user)
    else:
        answer.upvotes.add(request.user)
        answer.downvotes.remove(request.user)

    return django.http.HttpResponseRedirect(
        answer.topic.get_absolute_url(),
    )


def downvote(request):
    answer = django.shortcuts.get_object_or_404(
        forum.models.Answer,
        id=request.POST.get("answer_id"),
    )

    if answer.downvotes.filter(id=request.user.id).exists():
        answer.downvotes.remove(request.user)
    else:
        answer.downvotes.add(request.user)
        answer.upvotes.remove(request.user)

    return django.http.HttpResponseRedirect(
        answer.topic.get_absolute_url(),
    )


@django.contrib.auth.decorators.login_required(login_url="/login/")
def topic_report(request, topic_id):
    topic = django.shortcuts.get_object_or_404(
        forum.models.Topic,
        id=topic_id,
    )

    if request.method == "POST":
        form = forum.forms.TopicReportForm(
            request.POST or None,
        )
        if form.is_valid():
            reason = form.cleaned_data["reason"]

            forum.models.TopicReport.objects.create(
                reporter=request.user,
                reason=reason,
                topic=topic,
            )
            return django.shortcuts.redirect("forum:forum")
    else:
        form = forum.forms.TopicReportForm()

    return django.shortcuts.render(
        request,
        "forum/topic_report.html",
        {"form": form},
    )


@django.contrib.auth.decorators.login_required(login_url="/login/")
def answer_report(request, ans_id):
    answer = django.shortcuts.get_object_or_404(
        forum.models.Answer,
        id=ans_id,
    )

    if request.method == "POST":
        form = forum.forms.AnswerReportForm(
            request.POST or None,
        )
        if form.is_valid():
            reason = form.cleaned_data["reason"]

            forum.models.AnswerReport.objects.create(
                reporter=request.user,
                reason=reason,
                answer=answer,
            )
            return django.shortcuts.redirect("forum:forum")
    else:
        form = forum.forms.AnswerReportForm()

    return django.shortcuts.render(
        request,
        "forum/answer_report.html",
        {"form": form},
    )
