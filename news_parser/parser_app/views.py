from django.shortcuts import render, redirect
from .models import *
# from .forms import *
from .modules.get_info import *


# Create your views here.
def parsing(request):
    if request.method == 'POST':
        N = News()
        N.get_links()
        N.get_data()
    return redirect('home')


def index(request):
    articles = Articles.objects.all().order_by('-id')
    context = {
        'title': 'Main',
        'articles': articles,
    }
    return render(request, 'parser_app/index.html', context)


def account(request):
    context = {
        'title': 'Account',
    }
    return render(request, 'parser_app/account.html', context)
