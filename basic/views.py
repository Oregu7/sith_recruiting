from django.shortcuts import render


def index(request):
    return render(request, 'basic/homePage.html')