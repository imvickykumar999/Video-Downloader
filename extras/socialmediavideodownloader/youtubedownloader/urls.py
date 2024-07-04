from django.urls import path
from . import views

app_name = 'youtubedownloader'

urlpatterns = [
    path('', views.download_view, name='index'),
    path('formats/', views.download_view, name='formats'),
    path('download/', views.download_selected_view, name='download'),
]
