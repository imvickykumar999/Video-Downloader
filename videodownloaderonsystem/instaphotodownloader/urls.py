from django.urls import path
from .views import index

app_name = 'instaphotodownloader'

urlpatterns = [
    path('', index, name='index'),
]
