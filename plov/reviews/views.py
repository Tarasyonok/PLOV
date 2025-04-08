import json

import django.contrib.auth.mixins
import django.contrib.messages.views
import django.http
import django.template.loader
import django.urls
import django.views.generic

import reviews.forms
import reviews.models


class ReviewListView(django.views.generic.ListView):
    model = reviews.models.Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return reviews.models.Review.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_review'] = reviews.models.Review.objects.filter(user=self.request.user).first()
            context['is_creating_review'] = self.request.headers.get('HX-Target') == 'review-form-container'

        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            self.template_name = 'reviews/partials/review_list.html'

        return super().get(request, *args, **kwargs)


class ReviewCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.contrib.messages.views.SuccessMessageMixin,
    django.views.generic.CreateView,
):
    model = reviews.models.Review
    form_class = reviews.forms.ReviewForm
    success_message = 'Your review was submitted successfully!'
    template_name = 'reviews/partials/review_form.html'
    success_url = django.urls.reverse_lazy('reviews:reviews')

    def test_func(self):
        course = self.request.user.courses.filter(specialization='D')
        return course.exists() and course.first().is_graduated

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        if self.request.headers.get('HX-Request'):
            # Return a proper HTMX response with multiple triggers
            response = django.http.HttpResponse(
                status=204,  # No Content - we're just triggering actions
                headers={
                    'HX-Trigger': json.dumps(
                        {'reviewSubmitted': True, 'showToast': {'message': self.success_message, 'type': 'success'}}
                    ),
                    'HX-Refresh': 'true',  # Full client-side refresh
                },
            )
        else:
            django.contrib.messages.success(self.request, self.success_message)

        return response

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return django.http.HttpResponse('You are not authorized to leave a review.', status=403)

        return super().get(request, *args, **kwargs)


class ReviewUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.contrib.messages.views.SuccessMessageMixin,
    django.views.generic.UpdateView,
):
    model = reviews.models.Review
    form_class = reviews.forms.ReviewForm
    success_message = 'Review updated successfully!'
    template_name = 'reviews/partials/review_form.html'
    success_url = django.urls.reverse_lazy('reviews:reviews')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.headers.get('HX-Request'):
            # Return a proper HTMX response with multiple triggers
            response = django.http.HttpResponse(
                status=204,  # No Content - we're just triggering actions
                headers={
                    'HX-Trigger': json.dumps(
                        {'reviewUpdated': True, 'showToast': {'message': self.success_message, 'type': 'success'}}
                    ),
                    'HX-Refresh': 'true',  # Full client-side refresh
                },
            )
        else:
            django.contrib.messages.success(self.request, self.success_message)

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review'] = self.get_object()  # Pass review to template for 'Update' button text
        return context


class ReviewDeleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.contrib.messages.views.SuccessMessageMixin,
    django.views.generic.DeleteView,
):
    model = reviews.models.Review
    success_message = 'Review deleted successfully!'
    template_name = 'reviews/partials/review_list.html'
    success_url = django.urls.reverse_lazy('reviews:reviews')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        # Store review ID before deletion for client-side handling
        review_id = self.get_object().id

        response = super().delete(request, *args, **kwargs)

        if request.headers.get('HX-Request'):
            # Return a lightweight response with triggers
            return django.http.HttpResponse(
                status=204,  # No Content
                headers={
                    'HX-Trigger': json.dumps(
                        {'reviewDeleted': review_id, 'showToast': {'message': self.success_message, 'type': 'success'}}
                    ),
                    'HX-Refresh': 'true',  # Let client handle the refresh
                },
            )
        else:
            django.contrib.messages.success(request, self.success_message)

        return response
