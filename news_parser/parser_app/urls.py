from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('account/', account, name='account'),
    path('parsing/', parsing, name='parsing')
]
