import django.forms

import stickers.models


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            'widget',
            MultipleFileInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Прикрепите фотографии стикеров, которые будут находиться в этом стикерпаке',
                },
            ),
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return [single_file_clean(data, initial)]


class StickerPackForm(django.forms.ModelForm):
    stickers = MultipleFileField()

    class Meta:
        model = stickers.models.StickerPack
        fields = ['name', 'stickers']

class StickerForm(django.forms.ModelForm)
    class Meta:
        model = stickers.models.Sticker
        fields = ['image']
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        
        if not image:
            self.add_error('image', 'Please select a sticker image')
        else:
            extension = image.name.split('.')[-1].lower()
            if extension not in stickers.constants.IMAGE_EXTENSIONS:
                self.add_error('image', 'Invalid image file format')
        
        return cleaned_data