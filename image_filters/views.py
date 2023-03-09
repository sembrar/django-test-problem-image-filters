from django.shortcuts import render, get_object_or_404, redirect
from .forms import ImageUploadForm, ApplyFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .models import UploadedImages, FilteredImage
from django.contrib.auth.models import User
from django.conf import settings
import os
import cv2


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


def apply_filter(request, **kwargs):  # kwargs will be a dict with a key "pk" whose corresponding value is image-id
    # see the comments in "register" function in "users/views.py", because, the logic used below is exactly similar

    image_obj = get_object_or_404(UploadedImages, id=kwargs["pk"])
    image_url = image_obj.image.url

    if request.method == "POST":
        form = ApplyFilterForm(request.POST)

        if form.is_valid():
            filtered_image, filter_name_to_save = get_filtered_image(request, image_obj.image.path)
            messages.success(request, f"{filter_name_to_save} applied successfully")

            if 'save_button' in request.POST:
                # Save button is clicked, image must be saved along with the filter applied

                # create save directory if it doesn't exist (media/save/)
                save_dir = os.path.join(settings.MEDIA_ROOT, "save")
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)

                # generate the unique name of the filtered file: (username + filter_name + image_name)
                img_save_name = f"{request.user.username}" \
                                f"-{filter_name_to_save.replace(':', '-')}" \
                                f"-{image_obj.image.name}"

                # save the filtered image
                img_save_path = os.path.join(save_dir, img_save_name)
                cv2.imwrite(img_save_path, filtered_image)

                # generate the filtered image url, so that, at the bottom of the function, it is passed in context,
                # and the filtered image is shown on screen
                filtered_image_url = os.path.join(settings.MEDIA_URL, f"save/{img_save_name}")

                # save a "FilteredImage" model object:
                FilteredImage(owner=request.user, file_name=img_save_name, filter_name=filter_name_to_save,
                              original_img=image_obj).save()

            else:
                # Preview button is clicked, save it in a temporary spot display it on the page

                # create temporary save directory (media/temp/)
                temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
                if not os.path.isdir(temp_dir):
                    os.makedirs(temp_dir)

                # save the filtered image
                temp_img_save_path = os.path.join(temp_dir, f"{request.user.username}-{image_obj.image.name}")
                cv2.imwrite(temp_img_save_path, filtered_image)

                # generate the filtered image url, so that, at the bottom of the function, it is passed in context,
                # and the filtered image is shown on screen
                filtered_image_url = os.path.join(settings.MEDIA_URL, f"temp/{request.user.username}-{image_obj.image.name}")

            image_url = filtered_image_url  # this is used in the "context" argument at the bottom of the function

            # (discarded) redirect here, or else, browser will ask "resubmit?" if user pressed refresh
            # return redirect(request.path)  # discarded as it clears the form, (user shouldn't press refresh instead)
        else:
            messages.error(request, f"Apply filter failed.")
    else:
        form = ApplyFilterForm()
    return render(request, "image_filters/apply-filter.html", {"form": form, "image_url": image_url})


def get_filtered_image(request, original_image_path):
    # form data is valid in the request (except may be even numbers for kernel size)

    filter_type = request.POST["filters"]

    if filter_type == "grayscale":

        filtered_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
        filter_name_to_save = "Grayscale"

    elif filter_type == "sepia":

        img = cv2.imread(original_image_path, cv2.IMREAD_COLOR)

        # the following sepia is learnt from: https://stackoverflow.com/questions/1061093/how-is-a-sepia-tone-created
        b = img[:, :, 0]
        g = img[:, :, 1]
        r = img[:, :, 2]
        filtered_image = cv2.multiply(img, 0)
        filtered_image[:, :, 0] = cv2.add(cv2.add(cv2.multiply(r, 0.272), cv2.multiply(g, 0.534)), cv2.multiply(b, 0.131))
        filtered_image[:, :, 1] = cv2.add(cv2.add(cv2.multiply(r, 0.349), cv2.multiply(g, 0.686)), cv2.multiply(b, 0.168))
        filtered_image[:, :, 2] = cv2.add(cv2.add(cv2.multiply(r, 0.393), cv2.multiply(g, 0.769)), cv2.multiply(b, 0.189))

        filter_name_to_save = "Sepia"

    elif filter_type == "gaussian_blur":
        kernel_size = int(request.POST["gaussian_filter_kernel_size"])
        # Gaussian blur requires that kernel size be odd. So, if it is even, we subtract 1.
        # The form makes sure that the least value we get is 3 and the highest value is 99.
        # So, subtraction when it's an odd number will never make it 0.
        if kernel_size % 2 == 0:
            kernel_size -= 1

        img = cv2.imread(original_image_path, cv2.IMREAD_UNCHANGED)

        filtered_image = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        filter_name_to_save = f"Gaussian Blur with kernel size {kernel_size}"

    else:

        thresh1 = int(request.POST["canny_edge_detection_filter_threshold1"])
        thresh2 = int(request.POST["canny_edge_detection_filter_threshold2"])
        aperture_size = int(request.POST["canny_edge_detection_filter_apertureSize"])
        use_l2gradient = request.POST["canny_edge_detection_filter_gradient"] == "l2gradient"

        grayscale = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
        filtered_image = cv2.Canny(grayscale, thresh1, thresh2,
                                   apertureSize=aperture_size, L2gradient=use_l2gradient)

        filter_name_to_save = f"Canny Edge Detection with thresholds:({thresh1},{thresh2})," \
                              f" apertureSize:{aperture_size}, Gradient:L{2 if use_l2gradient else 1}"

    return filtered_image, filter_name_to_save


class UserFilteredImagesListView(ListView):
    # a ListView is a generic class view that takes a Model that it queries and shows as list

    model = FilteredImage
    template_name = "image_filters/filtered-images.html"
    context_object_name = "filtered_images"  # this is the variable name that will be available in the template
    extra_context = {"filtered_image_root_url": os.path.join(settings.MEDIA_URL, "save")}

    # we overload the following method to filter the images by "user", so that,
    # only the images uploaded by current user are sent to the template html
    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return super().get_queryset().filter(owner=user)
        # todo, in the above, .order_by('-date_posted') after adding that field to the UploadedImages Model
