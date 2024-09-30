from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from .models import Articles
from django.http import JsonResponse
from .modules.get_info import *
from datetime import datetime
from django.urls import reverse

date_format = "%H:%M, %d.%m.%y"


def parse_published(article):
    try:
        return datetime.strptime(article.published, date_format)
    except ValueError:
        return None


# Create your views here.
def parsing(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword", "")
        N = News()
        if keyword:
            N.get_links(keyword)
        else:
            N.get_links()
        N.get_data()
        return redirect(f"{reverse('parser_app:index')}?keyword={keyword}")
    return redirect("parser_app:index")


def index(request):
    # Fetch filter parameters from GET request
    keyword = request.GET.get("keyword", "")
    sort_order = request.GET.get("sort", "newer")

    # Build the queryset based on filters
    articles = Articles.objects.all()

    # Filter articles by keyword if provided
    if keyword:
        articles = articles.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )

    # Sort articles by published date
    articles = sorted(articles, key=lambda article: parse_published(article))

    # Reverse the order if sort_order is "newer"
    if sort_order == "newer":
        articles.reverse()

    # Set up pagination
    paginator = Paginator(articles, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Update the context with the filtered articles
    context = {
        "title": "Main",
        "articles": page_obj,  # Change here to use page_obj for correct pagination
        "page_obj": page_obj,
        "keyword": keyword,
        "sort_order": sort_order,
    }

    return render(request, "parser_app/index.html", context)


@login_required
def save_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    user = request.user

    if article in user.saved_articles.all():
        # Remove article from saved
        request.user.saved_articles.remove(article)
        return JsonResponse({"saved": False})
    else:
        # Save article
        request.user.saved_articles.add(article)
        return JsonResponse({"saved": True})


def article_detail(request, article_id):
    article = get_object_or_404(Articles, id=article_id)

    context = {"title": article.name, "article": article}

    return render(request, "parser_app/article_detail.html", context)
