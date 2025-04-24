import django.contrib.auth.decorators
import django.contrib.auth.mixins
import django.contrib.contenttypes.models
import django.contrib.messages.views
import django.http
import django.shortcuts
import django.urls
import django.views.decorators.http
import django.views.generic

import interactions.models
import reviews.models


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_POST
def vote_review(request, review_id):
    review = django.shortcuts.get_object_or_404(reviews.models.Review, pk=review_id)
    vote_type = request.POST.get('vote_type')

    if vote_type not in ['U', 'D']:
        return django.http.JsonResponse({'error': 'Invalid vote type'}, status=400)

    content_type = django.contrib.contenttypes.models.ContentType.objects.get_for_model(review)

    vote, created = interactions.models.Vote.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=review.id,
        defaults={'vote_type': vote_type},
    )

    if not created:
        if vote.vote_type == vote_type:
            vote.delete()
        else:
            vote.vote_type = vote_type
            vote.save()

    context = {
        'review': review,
        'user_vote': vote.vote_type if not created and vote.vote_type == vote_type else None,
    }

    if request.htmx:
        return django.shortcuts.render(
            request,
            'reviews/partials/vote_controls.html',
            {
                'review': review,
                'user_vote': vote_type if (created or vote.vote_type == vote_type) else None,
            },
        )

    return django.http.JsonResponse(
        {'upvotes': review.upvotes_count, 'downvotes': review.downvotes_count, 'user_vote': context['user_vote']},
    )
