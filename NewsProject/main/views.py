from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse(' Главная страница ')


def about(request):
    return HttpResponse(' О сайте ')


def contacts(request):
    return HttpResponse(' Наши контакты ')
