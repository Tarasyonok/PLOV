import django.forms

import reviews.models


class ReviewForm(django.forms.ModelForm):
    class Meta:
        model = reviews.models.Review
        fields = ['rating', 'content']
        widgets = {
            'content': django.forms.Textarea(attrs={'rows': 4}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise django.forms.ValidationError('Rating must be between 1 and 5')

        return rating
