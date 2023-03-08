from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="image-filters-home"),
    path('upload/', views.upload_image, name="image-filters-upload"),
    path('uploaded-images/', views.UserUploadedImagesListView.as_view(), name="image-filters-uploaded-images"),
    path('apply-filter/<int:pk>/', views.apply_filter, name="image-filters-apply-filter"),
]
