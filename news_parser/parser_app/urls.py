from django.urls import path
from . import views

app_name = "parser_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('parsing/', views.parsing, name='parsing'),
    path('save_article/<int:article_id>/', views.save_article, name="save_article")
]
