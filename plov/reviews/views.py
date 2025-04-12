import django.contrib.auth.mixins
import django.contrib.messages.views
import django.urls
import django.views.generic
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

import reviews.forms
import reviews.models
from interactions.models import Vote


class BaseReviewView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.contrib.messages.views.SuccessMessageMixin,
):
    model = reviews.models.Review
    success_url = django.urls.reverse_lazy('reviews:reviews')


class ReviewListView(django.views.generic.ListView):
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return reviews.models.Review.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_review'] = reviews.models.Review.objects.filter(user=self.request.user).first()
            context['form'] = reviews.forms.ReviewForm()
        return context


class ReviewCreateView(BaseReviewView, django.views.generic.CreateView):
    form_class = reviews.forms.ReviewForm
    success_message = "Your review was submitted successfully!"

    def test_func(self):
        course = self.request.user.courses.filter(specialization="D")
        return course.exists() and course.is_graduated

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(BaseReviewView, django.views.generic.UpdateView):
    form_class = reviews.forms.ReviewForm
    success_message = "Review updated successfully!"

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user


class ReviewDeleteView(BaseReviewView, django.views.generic.DeleteView):
    success_message = "Review deleted successfully!"

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        from django.contrib import messages

        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required
@require_POST
def vote_review(request, review_id):
    review = get_object_or_404(reviews.models.Review, pk=review_id)
    vote_type = request.POST.get('vote_type')

    if vote_type not in [choice[0] for choice in Vote.VoteChoices.choices]:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)

    content_type = ContentType.objects.get_for_model(review)

    # Check if vote exists
    vote, created = Vote.objects.get_or_create(
        user=request.user, content_type=content_type, object_id=review.id, defaults={'vote_type': vote_type}
    )

    if not created:
        if vote.vote_type == vote_type:
            # User clicked same vote again - remove vote
            vote.delete()
        else:
            # User changed vote type
            vote.vote_type = vote_type
            vote.save()

    context = {'review': review, 'user_vote': vote.vote_type if not created and vote.vote_type == vote_type else None}

    if request.htmx:
        return render(request, 'reviews/partials/vote_controls.html', context)

    return JsonResponse(
        {  # Fallback for non-HTMX
            'upvotes': review.upvotes_count,
            'downvotes': review.downvotes_count,
            'user_vote': context['user_vote'],
        }
    )
