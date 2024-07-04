import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FacebookStoryForm
from .models import FacebookStoryDownload
import yt_dlp
from datetime import datetime
from django.conf import settings

def download_facebook_story(url, output_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/{timestamp}.%(ext)s',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return f"{timestamp}.mp4"  # Return file name
        except yt_dlp.utils.DownloadError as e:
            return None

def index(request):
    if request.method == 'POST':
        form = FacebookStoryForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            output_dir = os.path.join(settings.MEDIA_ROOT, 'facebook_stories')
            os.makedirs(output_dir, exist_ok=True)
            file_name = download_facebook_story(url, output_dir)
            if file_name:
                download = FacebookStoryDownload(url=url, file_path=file_name)
                download.save()
                video_url = os.path.join(settings.MEDIA_URL, 'facebook_stories', file_name)
                return render(request, 'fbstorydownloader/download.html', {'video_url': video_url})
            else:
                return HttpResponse("Failed to download the story.", status=500)
    else:
        form = FacebookStoryForm()
    return render(request, 'fbstorydownloader/index.html', {'form': form})
