from django.urls import path
from . import views

app_name = "parser_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('parsing/', views.parsing, name='parsing')
]
