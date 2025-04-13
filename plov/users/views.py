import django.conf
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.messages.views
import django.urls
import django.views.generic

import users.forms
import users_status.models


class SignUpView(
    django.contrib.messages.views.SuccessMessageMixin,
    django.views.generic.FormView,
):
    template_name = 'users/signup.html'
    form_class = users.forms.SignUpForm
    success_url = django.urls.reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = True
        new_user.save()
        return super().form_valid(form)


class PublicProfileView(django.views.generic.DetailView):
    template_name = 'users/public_profile.html'
    model = django.contrib.auth.get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object
        context['is_online'] = users_status.models.UserStatus.is_user_online(
            self.kwargs['username'],
        )
        context['last_seen'] = users_status.models.UserStatus.last_seen(
            self.kwargs['username'],
        )
        return context


class PrivateProfileEditView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.UpdateView):
    template_name = 'users/profile_edit.html'
    form_class = users.forms.ProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_instance'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        return django.urls.reverse_lazy('users:profile', args=[self.request.user.username])
