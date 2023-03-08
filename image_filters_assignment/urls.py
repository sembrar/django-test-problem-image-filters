"""image_filters_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# the following two lines are from
# https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('image_filters.urls')),
    path('user/', include('users.urls')),
    path('admin/', admin.site.urls),
]

# the following line (though a little bit modified) is also from
# https://docs.djangoproject.com/en/4.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
# fixme they suggest this way for serving user uploaded files during development,
#  but they suggest another way for production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
