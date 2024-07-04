import os
from django.shortcuts import render
from django.conf import settings

def home_view(request):
    video_dir = settings.MEDIA_ROOT
    video_files = [f for f in os.listdir(video_dir)]
    video_urls = [os.path.join(settings.MEDIA_URL, f) for f in video_files]
    videos = zip(video_files, video_urls)
    return render(request, 'home.html', {'videos': videos})

