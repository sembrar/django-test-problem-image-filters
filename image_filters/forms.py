from django import forms
from .models import UploadedImages


class ImageUploadForm(forms.ModelForm):  # this is a class based form

    class Meta:
        model = UploadedImages  # the model to work with
        fields = ['image']  # the fields that the form should show

    def save(self, commit=True, user=None):  # As every uploaded image is associated with a user (User is foreign-key),
        # we override the form's save method, so that, we can provide it with the current logged-in user
        self.instance.owner = user
        return super().save(commit)
