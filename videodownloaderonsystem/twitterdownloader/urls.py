from django.urls import path
from .views import index, download_selected_view

app_name = 'twitterdownloader'

urlpatterns = [
    path('', index, name='index'),
    path('download/', download_selected_view, name='download'),
]
