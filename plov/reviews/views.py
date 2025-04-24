import json

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


class BaseReviewView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.contrib.messages.views.SuccessMessageMixin,
    django.views.generic.detail.SingleObjectMixin,
):
    model = reviews.models.Review
    success_url = django.urls.reverse_lazy('reviews:reviews')


class ReviewListView(django.views.generic.ListView):
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

    def get_template_names(self):
        if self.request.htmx:
            return ['reviews/partials/reviews_list_content.html']

        return [self.template_name]

    def get_queryset(self):
        return reviews.models.Review.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_review = reviews.models.Review.objects.filter(user=self.request.user).first()
            context['user_review'] = user_review
            context['show_write_button'] = not user_review
            context['form'] = reviews.forms.ReviewForm()

        return context


class ReviewCreateView(BaseReviewView, django.views.generic.edit.CreateView):
    form_class = reviews.forms.ReviewForm
    template_name = 'reviews/partials/review_form.html'

    def test_func(self):
        course = self.request.user.courses.filter(specialization='D')
        return course.exists() and course.first().is_graduated

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.htmx:
            if form.is_valid():
                self.object = form.save()
                response = django.http.HttpResponse(status=204)
                response['HX-Trigger'] = json.dumps(
                    {
                        'refreshReviews': True,
                        'hideWriteButton': True,
                    },
                )

                return response

        return super().form_valid(form)


class ReviewUpdateView(BaseReviewView, django.views.generic.edit.UpdateView):
    form_class = reviews.forms.ReviewForm
    template_name = 'reviews/partials/review_form.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.htmx:
            kwargs['initial'] = {
                'rating': self.object.rating,
                'content': self.object.content,
            }

        return kwargs

    def form_valid(self, form):
        if self.request.htmx:
            if form.is_valid():
                self.object = form.save()
                response = django.shortcuts.HttpResponse(status=204)
                response['HX-Trigger'] = json.dumps(
                    {
                        'refreshReviews': True,
                        'hideWriteButton': True,
                    },
                )
                return response

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.object = self.get_object()
            return django.shortcuts.render(
                request,
                'reviews/partials/review_form.html',
                {
                    'form': self.get_form(),
                    'review': self.object,
                },
            )

        return super().get(request, *args, **kwargs)


class ReviewDeleteView(BaseReviewView, django.views.generic.edit.DeleteView):
    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.htmx:
            self.object.delete()
            return django.http.HttpResponse(status=204, headers={'HX-Trigger': json.dumps({'reviewDeleted': True})})

        return super().delete(request, *args, **kwargs)
