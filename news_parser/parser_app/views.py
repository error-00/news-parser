from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .modules.get_info import *
from django.contrib.auth.decorators import login_required
from .models import Articles
from django.http import JsonResponse

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

@login_required
def save_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    user = request.user

    if article in user.saved_articles.all():
        # Remove article from saved
        request.user.saved_articles.remove(article)
        return JsonResponse({'saved': False})
    else:
        # Save article
        request.user.saved_articles.add(article)
        return JsonResponse({'saved': True})
    