from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import *
# from .forms import *
from .modules.get_info import *


# Create your views here.
def parsing(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        N = News()
        if keyword:
            N.get_links(keyword)
        else:
            N.get_links()
        N.get_data()
    return redirect('parser_app:index')


def index(request):
    articles = Articles.objects.all().order_by('-id')
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Main',
        'articles': articles,
        'page_obj': page_obj,
    }
    return render(request, 'parser_app/index.html', context)

