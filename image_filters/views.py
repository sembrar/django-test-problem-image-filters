from django.shortcuts import render, get_object_or_404, redirect
from .forms import ImageUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import UploadedImages
from django.contrib.auth.models import User


def home(request):
    return render(request, "image_filters/home.html")


@login_required  # this decorator first takes us to login page if any user tries to go to upload page without logging in
def upload_image(request):
    # see the comments in "register" function in "users/views.py", because, the logic used below is exactly similar

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)  # request.FILES has image data. form is invalid without it
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, f'Image "{request.FILES.get("image")}" uploaded successfully.'
                                      f' Upload another or navigate to home page using navbar.')

            return redirect('image-filters-upload')  # we redirect to the same upload form,
            # because, we want the user to be able to upload any number of images one by one.
            # Also, we must redirect, because, if we instead let it go to the render function, even though it renders
            # the same upload form, if the user refreshes the page, the browser says "Do you want to re-submit?"
        else:
            messages.error(request, f"Image upload failed. Please see the error message below and try again.")
    else:
        form = ImageUploadForm()

    return render(request, "image_filters/upload.html", {'form': form})


class UserUploadedImagesListView(ListView):
    # a ListView is a generic class view that takes a Model that it queries and shows as list

    model = UploadedImages
    template_name = "image_filters/uploaded-images.html"
    context_object_name = "uploaded_images"  # this is the variable name that will be available in the template

    # we overload the following method to filter the images by "user", so that,
    # only the images uploaded by current user are sent to the template html
    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return super().get_queryset().filter(owner=user)
        # todo, in the above, .order_by('-date_posted') after adding that field to the UploadedImages Model
