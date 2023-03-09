from django.db import models
from django.contrib.auth.models import User


class UploadedImages(models.Model):
    image = models.ImageField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # in the above, one user can own many images (one to many relationship), and one image can have at most one owner
    # "on_delete = CASCADE" makes sure that if a user is deleted, all their images are deleted as well


class FilteredImage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    filter_name = models.CharField(max_length=100)
    original_img = models.ForeignKey(UploadedImages, on_delete=models.CASCADE)
