from django.shortcuts import render


def home(request):
    return render(request, "image_filters/home.html")
