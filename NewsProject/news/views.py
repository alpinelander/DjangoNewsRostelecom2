from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
# Create your views here.
from .forms import *

import json
def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term','')
        articles = Article.objects.filter(title__icontains=q)
        results =[]
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def search(request):
    # try:
    #     del request.session['selected_author']
    # except:
    #     pass
    # try:
    #     del request.session['selected_category']
    # except:
    #     pass
    if request.method == 'POST': #пришел запрос из бокового меню
        value = request.POST['search_input']  # находим новости
        articles = Article.objects.filter(title__icontains=value)
        request.session['search_input'] = value
        if len(articles) == 1: #если одна- сразу открываем подробное отображение новости
            return render(request, 'news/news_detail.html', {'article': articles[0]})
            #return redirect('news')
            #либо через фрагмент URLссылки:
            # но в таком случае придётся обрабатывать ссылку в Urls
            #функция reverse из модуля Urls добавит переданные аргументы в качестве get-аргументов.
            # return redirect(reverse('news', kwargs={'search_input':value}))

            # return render(request, 'news/news_list.html', {'articles': articles})
    value = request.session.get('search_input')
    articles = Article.objects.filter(title__icontains=value)
    articles = articles.order_by('-date')
    total = len(articles)
    p = Paginator(articles, 2)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    title = _(f'Результаты по запросу: {value}')
    context = {'articles': page_obj,
               'total': total,
               'title': title
               }
    return render(request, 'news/news_search_list.html', context)


from .utils import ViewCountMixin
class ArticleDetailView(ViewCountMixin,DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

class ArticleDeleteView(DeleteView):
    success_url = reverse_lazy('news_index')
    model = Article
    template_name = 'news/delete_article.html'


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text','tags']

from django.conf import settings
@login_required(login_url=settings.LOGIN_URL)
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #проверили что не аноним

                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m()
                form = ArticleForm()
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img,title=img.name)

                return redirect('news')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})

#def news(request):
#   return HttpResponse(' Главная страница ')
#    return render(request, 'news/news.html')

# def index(request):
#     article = Article.objects.all().first()
#     context = {'article':article}
#     return render(request, 'news/index.html', context)

from time import time
from django.core.paginator import Paginator
from django.db.models import Count
# def pagination(request):
#     articles = Article.objects.all()
from django.utils.translation import gettext as _
def index(request):
    selected_author = request.session.get('author_filter')
    selected_category = request.session.get('category_filter')
    selected_author = 0 if selected_author == None else selected_author
    selected_category = 0 if selected_category == None else selected_category

    categories = Article.categories #создали перечень категорий
    author_list = User.objects.filter(article__isnull=False).distinct() #создали перечень авторов не пустых
    if request.method == "POST": #при обработке POST - мы только сохраняяем в сессию выбранных авторов
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        request.session['author_filter'] = selected_author
        request.session['category_filter'] = selected_category
        return redirect('news')
    else: #если страница открывется впервые или нас переадресовала сюда функция поиск
        articles = Article.objects.all()
        if selected_author != 0:  # если не пустое - находим нужные ноновсти
            articles = articles.filter(author=selected_author)
        if selected_category != 0:  # фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category - 1][0])

    #сортировка от свежих к старым новостям
    articles=articles.order_by('-date')
    total = len(articles)
    p = Paginator(articles,2)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    title = _('Заголовок страницы новости-индекс')

    context = {'articles': page_obj, 'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category, 'total':total,
               'title':title
               }

    return render(request,'news/news_list.html',context)


# def add_news(request):
#     author = User.objects.get(id=request.user.id)
#     article = Article(author=author, title='Заголовок новости',
#                       anouncement='кратко о новости', text='Текст новости')
#     article.save()
#     context = {'article':article}
#     return HttpResponse(f'добавлена новость <h1>{ article.title }<h1/>')

def news_slider(request):
    articles = Article.objects.all()
    #сортировка от свежих к старым новостям
    articles=articles.order_by('-date')
    total = len(articles)
    context = {'articles': articles,'total':total,}

    return render(request,'news/news_slider.html',context)