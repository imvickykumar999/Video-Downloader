from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('youtubedownloader/', include('youtubedownloader.urls')),
    path('instadownloader/', include('instadownloader.urls')),
    path('facebookdownloader/', include('facebookdownloader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

