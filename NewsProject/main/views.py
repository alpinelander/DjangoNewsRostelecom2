from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound


# Create your views here.
def index(request):
#   return HttpResponse(' Главная страница ')
    return render(request, 'main/index.html')

def about(request):
    return HttpResponse(' О сайте ')

def contacts(request):
    return HttpResponse(' Наши контакты ')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")