import forum.models


def topics_context(request):
    topics = forum.models.Topic.objects.all()
    main_topics = topics.order_by('-created')[:3]
    context = {'main_topics': main_topics}
    return context


def my_topics_counter_context(request):
    if request.user.is_authenticated:
        topics = forum.models.Topic.objects.filter(user=request.user)
        my_topics = topics.count()
        context = {'my_topics': my_topics}
        return context

    return {'none': None}
