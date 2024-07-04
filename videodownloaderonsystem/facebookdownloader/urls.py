from django.urls import path
from .views import index, download_view

app_name = 'facebookdownloader'

urlpatterns = [
    path('', index, name='index'),
    path('download/', download_view, name='download_view'),
]
