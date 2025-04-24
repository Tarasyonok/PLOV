import django.contrib.auth.decorators
import django.contrib.auth.mixins
import django.contrib.contenttypes.models
import django.contrib.messages.views
import django.http
import django.shortcuts
import django.urls
import django.views.decorators.http
import django.views.generic
import reviews.forms
import reviews.models

import interactions.models


@django.contrib.auth.decorators.login_required
@django.views.decorators.http.require_POST
def vote_review(request, review_id):
    review = django.shortcuts.get_object_or_404(reviews.models.Review, pk=review_id)
    vote_type = request.POST.get('vote_type')

    if vote_type not in ['U', 'D']:
        return django.http.JsonResponse({'error': 'Invalid vote type'}, status=400)

    content_type = django.contrib.contenttypes.models.ContentType.objects.get_for_model(review)

    try:
        existing_vote = interactions.models.Vote.objects.get(
            user=request.user, content_type=content_type, object_id=review.id
        )
    except interactions.models.Vote.DoesNotExist:
        existing_vote = None

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            existing_vote.delete()
            review.user_vote = None
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
            review.user_vote = vote_type
    else:
        interactions.models.Vote.objects.create(
            user=request.user, content_type=content_type, object_id=review.id, vote_type=vote_type
        )
        review.user_vote = vote_type

    # Refresh counts and set user_vote on the review object
    review.refresh_from_db()

    if request.htmx:
        return django.shortcuts.render(
            request,
            'reviews/partials/vote_controls.html',
            {
                'review': review,  # Now with user_vote attribute
            },
        )

    return django.http.JsonResponse(
        {
            'upvotes': review.upvotes_count,
            'downvotes': review.downvotes_count,
            'user_vote': review.user_vote,
        }
    )
