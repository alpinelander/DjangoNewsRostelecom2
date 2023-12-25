from django.shortcuts import render, HttpResponse
from .models import *
from .forms import *
# Create your views here.
def contact_page(request):
    form = ContactForm()
    context = {'form': form}
    return render(request,'users/contact_page.html',context)

def index(request):
    print(request.user,request.user.id)
    user_acc = Account.objects.get(user=request.user)
    print(user_acc, user_acc.birthdate, user_acc.gender)
    return HttpResponse('Приложение Users')
