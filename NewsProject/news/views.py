from django.shortcuts import render

# Create your views here.

def news(request):
#   return HttpResponse(' Главная страница ')
    return render(request, 'news/news.html')

