import django.conf
import django.contrib.auth
import django.contrib.auth.forms
import django.core.exceptions
import django.forms
import django.utils.timezone
import requests

import users.models
import users.utils.lms


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    class Meta:
        model = django.contrib.auth.get_user_model()

        fields = ['email', 'password1', 'password2', 'username']

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise django.forms.ValidationError(message='pwds')

        return cd['password']

    def clean_lms_profile_id(self):
        profile_id = self.cleaned_data.get('lms_profile_id')
        if not profile_id:
            return None

        try:
            client = users.utils.lms.LMSClient()
            profile_data = client.get_profile(profile_id)

            if not profile_data.get('is_active'):
                raise django.forms.ValidationError('This LMS profile is inactive')

            return profile_id
        except requests.exceptions.RequestException as e:
            raise django.forms.ValidationError(f'LMS Error: {str(e)}')


class UserEditForm(django.forms.ModelForm):
    class Meta:
        model = django.contrib.auth.get_user_model()
        fields = ['email', 'first_name', 'last_name', 'telegram_username', 'lms_profile_id']


class ProfileEditForm(django.forms.ModelForm):
    class Meta:
        model = users.models.UserProfile
        fields = ['avatar', 'bio', 'birthday']
        widgets = {
            'bio': django.forms.Textarea(
                attrs={
                    'rows': 4,
                }
            ),
            'birthday': django.forms.DateInput(
                attrs={
                    'type': 'date',
                    'max': str(django.utils.timezone.now().year - 10),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        self.user_form = UserEditForm(
            data=kwargs.get('data'), files=kwargs.get('files'), instance=user_instance, prefix='user'
        )

    def is_valid(self):
        return self.user_form.is_valid() and super().is_valid()

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5 * 1024 * 1024:
                raise django.forms.ValidationError(message='Max file size is 5MB')

        return avatar

    def save(self, commit=True):
        user = self.user_form.save(commit=commit)
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()

        return profile
