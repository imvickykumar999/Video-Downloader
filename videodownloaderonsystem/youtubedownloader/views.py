import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from yt_dlp import YoutubeDL
from django.conf import settings
import time
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    ydl_opts = {
        'format': '251+' + format_id,
        'outtmpl': os.path.join(output_dir, f'{timestamp}.%(ext)s'),
        'ffmpeg_location': r'C:\Users\surface\Documents\GitHub\Video-Downloader\ffmpeg-7.0.1-essentials_build\ffmpeg-7.0.1-essentials_build\bin',
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
        format_id = request.POST['format_id']
        output_dir = settings.YOUTUBE_DOWNLOAD_DIR
        os.makedirs(output_dir, exist_ok=True)
        video_file = download_video(url, format_id, output_dir)
        if video_file:
            class FileWrapper:
                def __init__(self, file_path):
                    self.file_path = file_path
                    self.file = open(file_path, 'rb')

                def __iter__(self):
                    return iter(self.file)

                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc_value, traceback):
                    self.file.close()
                    os.remove(self.file_path)

                def close(self):
                    self.file.close()
                    os.remove(self.file_path)

            response = FileResponse(FileWrapper(video_file))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_file)}"'
            return response
        else:
            return HttpResponse("Failed to download video.", status=500)
    return redirect('download_view')

