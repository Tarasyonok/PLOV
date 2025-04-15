import django.forms
import reviews.models


class ReviewForm(django.forms.ModelForm):
    class Meta:
        model = reviews.models.Review
        fields = ['rating', 'content']
        widgets = {
            'rating': django.forms.HiddenInput(),
            'content': django.forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True
        self.fields['rating'].error_messages = {'required': 'Please select a rating'}

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise django.forms.ValidationError('Rating must be between 1 and 5')

        return rating
