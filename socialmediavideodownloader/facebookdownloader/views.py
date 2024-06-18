import os
import yt_dlp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime

def index(request):
    if request.method == 'POST':
        url = request.POST['url']
        formats = list_formats(url)
        if formats:
            return render(request, 'facebookdownloader/formats.html', {'formats': formats, 'url': url})
        else:
            return HttpResponse("Failed to retrieve video formats.", status=500)
    return render(request, 'facebookdownloader/index.html')

def list_formats(url):
    try:
        ydl_opts = {
            'listformats': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            format_list = [{'format_id': f['format_id'], 'ext': f['ext'], 'note': f.get('format_note', 'No note available'), 'filesize': f.get('filesize', 'Unknown size')} for f in formats]
            return format_list
    except yt_dlp.DownloadError as e:
        return []

def download_facebook_video(url, format_id, output_dir):
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = f"{output_dir}/{timestamp}.mp4"
        output_file = f"{output_dir}/{timestamp}_final.mp4"

        ydl_opts_video = {
            'format': f"{format_id}+bestaudio",
            'outtmpl': video_file,
            'merge_output_format': 'mp4'
        }

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])

        # Rename the final merged file
        os.rename(video_file, output_file)

        return True, f"{timestamp}_final.mp4"
    except yt_dlp.DownloadError as e:
        return False, f"Error downloading video: {e}"

def download_view(request):
    if request.method == 'POST':
        url = request.POST['url']
        format_id = request.POST['format_id']
        output_dir = settings.MEDIA_ROOT
        success, filename = download_facebook_video(url, format_id, output_dir)
        if success:
            video_path = os.path.join(settings.MEDIA_URL, filename)
            return render(request, 'facebookdownloader/download.html', {'video_path': video_path})
        else:
            return HttpResponse(filename, status=500)
    return redirect('index')
