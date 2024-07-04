import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InstagramStoryForm
from .models import InstagramStoryDownload
import yt_dlp
from datetime import datetime
from django.conf import settings

def download_instagram_story(url, output_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/{timestamp}.%(ext)s',
        'quiet': True,
        # 'cookiesfrombrowser': ('chrome',),
        'ffmpeg_location': r'C:\Users\surface\Documents\GitHub\Video-Downloader\ffmpeg-7.0.1-essentials_build\ffmpeg-7.0.1-essentials_build\bin',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return f"{timestamp}.mp4"  # Return file name
        except yt_dlp.utils.DownloadError as e:
            return None

def index(request):
    if request.method == 'POST':
        form = InstagramStoryForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            output_dir = os.path.join(settings.MEDIA_ROOT, 'instagram_stories')
            os.makedirs(output_dir, exist_ok=True)
            file_name = download_instagram_story(url, output_dir)
            if file_name:
                download = InstagramStoryDownload(url=url, file_path=file_name)
                download.save()
                video_url = os.path.join(settings.MEDIA_URL, 'instagram_stories', file_name)
                return render(request, 'instastorydownloader/download.html', {'video_url': video_url})
            else:
                return HttpResponse("Failed to download the story.", status=500)
    else:
        form = InstagramStoryForm()
    return render(request, 'instastorydownloader/index.html', {'form': form})
