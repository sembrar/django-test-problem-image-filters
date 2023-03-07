from django.db import models
from django.contrib.auth.models import User


class UploadedImages(models.Model):
    image = models.ImageField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # in the above, one user can own many images (one to many relationship), and one image can have at most one owner
    # "on_delete = CASCADE" makes sure that if a user is deleted, all their images are deleted as well
