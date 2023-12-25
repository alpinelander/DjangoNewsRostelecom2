from django.shortcuts import render, HttpResponse
from .models import *
# Create your views here.

def news(request):
#   return HttpResponse(' Главная страница ')
    return render(request, 'news/news.html')

# def index(request):
#     article = Article.objects.all().first()
#     context = {'article':article}
#     return render(request, 'news/index.html', context)

def index(request):
    author_list = User.objects.all()
    selected = 0
    if request.method=="POST":
        selected = int(request.POST.get('author_filter'))
        if  selected == 0:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected)
    else:
        articles = Article.objects.all()
    context = {'articles':articles, 'author_list':author_list,'selected':selected }
    return render(request,'news/news_list.html',context)

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
