import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from yt_dlp import YoutubeDL
from django.conf import settings

def list_formats(url):
    ydl_opts = {'listformats': True}
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        
        format_list = []
        for f in formats[::-1]:
            format_id = f.get('format_id', 'N/A')
            ext = f.get('ext', 'N/A')
            format_note = f.get('format_note', 'N/A')
            filesize = f.get('filesize', 'Unknown size')
            format_str = f"{ext} - {format_note} - {filesize}"
            format_list.append({'id': format_id, 'description': format_str})
        return format_list

def download_video(url, format_id, output_dir):
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s')
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

def download_view(request):
    if request.method == 'POST':
        url = request.POST['url']
        format_list = list_formats(url)
        return render(request, 'youtubedownloader/formats.html', {'formats': format_list, 'url': url})
    return render(request, 'youtubedownloader/index.html')

def download_selected_view(request):
    if request.method == 'POST':
        url = request.POST['url']
        format_id = '251+' + request.POST['format_id']
        output_dir = settings.MEDIA_ROOT
        os.makedirs(output_dir, exist_ok=True)
        video_file = download_video(url, format_id, output_dir)
        video_url = os.path.join(settings.MEDIA_URL, os.path.basename(video_file))
        return render(request, 'youtubedownloader/download.html', {'video_url': video_url})
    return redirect('download_view')
