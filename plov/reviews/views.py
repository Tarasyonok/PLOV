import django.contrib.auth.mixins
import django.contrib.messages.views
import django.urls
import django.views.generic

import reviews.forms
import reviews.models


class BaseReviewView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.contrib.messages.views.SuccessMessageMixin,
):
    model = reviews.models.Review
    success_url = django.urls.reverse_lazy('reviews:reviews')


class ReviewListView(BaseReviewView, django.views.generic.ListView):
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return reviews.models.Review.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_review'] = reviews.models.Review.objects.filter(
                user=self.request.user
            ).first()
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