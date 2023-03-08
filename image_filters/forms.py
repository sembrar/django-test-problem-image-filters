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


class ApplyFilterForm(forms.Form):

    template_name_p = "image_filters/form-snippet-for-apply-filter.html"

    filters = forms.ChoiceField(
        choices=(
            ("grayscale", "Grayscale"),
            ("sepia", "Sepia"),
            ("gaussian_blur", "Gaussian Blur"),
            ("canny_edge_detection", "Canny Edge Detection"),
        ),
        widget=forms.RadioSelect,
    )

    gaussian_filter_kernel_size = forms.IntegerField(label="Kernel size", min_value=1, max_value=99, initial=5)

    canny_edge_detection_filter_threshold1 = forms.IntegerField(label="threshold1", max_value=255, min_value=0, initial=100)
    canny_edge_detection_filter_threshold2 = forms.IntegerField(label="threshold2", max_value=255, min_value=0, initial=200)
    canny_edge_detection_filter_apertureSize = forms.IntegerField(label="apertureSize", min_value=1, max_value=99, initial=3)
    canny_edge_detection_filter_gradient = forms.ChoiceField(
        label="gradient",
        choices=(
            ("l2gradient", "L2 Gradient"),
            ("l1gradient", "L1 Gradient"),
        ),
        widget=forms.RadioSelect,
        initial="l2gradient"
    )
