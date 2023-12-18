from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseNotFound


# Create your views here.
def index(request):
#   return HttpResponse(' Главная страница ')
    return render(request, 'main/index.html')

def about(request):
#    return HttpResponse(' О сайте ')
    return render(request, 'main/about.html')

def contacts(request):
#    return HttpResponse(' Наши контакты ')
    return render(request, 'main/contacts.html')

def sidebar(request):
    return render(request, 'main/sidebar.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1> Страница не найдена </h1>")