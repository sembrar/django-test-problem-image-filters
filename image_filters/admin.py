from django.contrib import admin
from .models import UploadedImages


admin.site.register(UploadedImages)  # so that the database table of UploadedImages is visible in the admin page
