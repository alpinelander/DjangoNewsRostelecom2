from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import *
@login_required(login_url="/")
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #проверили что не аноним

                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m()
                form = ArticleForm()

                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})

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
