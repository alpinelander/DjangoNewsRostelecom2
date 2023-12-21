from django.shortcuts import render, HttpResponse
from .models import *
# Create your views here.

def news(request):
#   return HttpResponse(' Главная страница ')
    return render(request, 'news/news.html')

def index(request):
    article = Article.objects.all().first()
    context = {'article':article}
    return render(request, 'news/index.html', context)

def detail(request,id):
    article = Article.objects.filter(id = id).first()
    context = {'article':article}
    return HttpResponse(f'Выводим конкретную новость <h1>{ article.title }<h1/>')

def add_news(request):
    author = User.objects.get(id=request.user.id)
    article = Article(author=author, title='Заголовок новости',
                      anouncement='кратко о новости', text='Текст новости')
    article.save()
    context = {'article':article}
    return HttpResponse(f'добавлена новость <h1>{ article.title }<h1/>')
