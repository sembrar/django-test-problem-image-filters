from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="image-filters-home"),
    path('upload/', views.upload_image, name="image-filters-upload"),
]
