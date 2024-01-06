from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView, UpdateView
# Create your views here.
from .forms import *



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

                return redirect('news_index')
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

def index(request):
    categories = Article.categories #создали перечень категорий
    author_list = User.objects.all() #создали перечень авторов
    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))
        request.session['selected_author'] = selected_author
        request.session['selected_category'] = selected_category
        if selected_author == 0: #выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0: #фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category-1][0])
    else: #если страница открывется впервые или нас переадресовала сюда функция поиск
        selected_author = request.session.get('selected_author')
        if selected_author != None: #если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(author=selected_author)
        else:
            selected_author = 0
        selected_category = 0
        value = request.session.get('search_input') #вытаскиваем из сессии значение поиска
        if value != None: #если не пустое - находим нужные новсти
            articles = Article.objects.filter(title__icontains=value)
            del request.session['search_input'] #чистим сессию, чтобы этот фильтр не "заело"
        else:
            #если не оказалось таокго ключика или запрос был кривой - отображаем все элементы
            articles = Article.objects.all()
    #сортировка от свежих к старым новостям
    articles=articles.order_by('-date')
    context = {'author_list':author_list, 'selected_author':selected_author,
               'categories':categories,'selected_category': selected_category,
               'articles':articles
               }

    return render(request,'news/news_list.html',context)


# def add_news(request):
#     author = User.objects.get(id=request.user.id)
#     article = Article(author=author, title='Заголовок новости',
#                       anouncement='кратко о новости', text='Текст новости')
#     article.save()
#     context = {'article':article}
#     return HttpResponse(f'добавлена новость <h1>{ article.title }<h1/>')
