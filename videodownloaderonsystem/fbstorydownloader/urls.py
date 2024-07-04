from django.urls import path
from .views import index

app_name = 'fbstorydownloader'

urlpatterns = [
    path('', index, name='index'),
]
