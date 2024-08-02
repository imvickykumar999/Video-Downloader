import os
import time
import yt_dlp
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, FileResponse
from mainapp.models import *

def list_formats(url):
    ydl_opts = {'listformats': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            thumbnail = info_dict.get('thumbnail', '')

            # Filter only video formats (excluding audio-only formats)
            video_formats = [f for f in formats if f.get('ext') == 'mp4'][:-3:-1]

            if not video_formats:
                return [], thumbnail

            # Select the first, middle, and last video formats
            high_format = video_formats[0]
            mid_format = video_formats[len(video_formats) // 2]
            low_format = video_formats[-1]
            
            selected_formats = [high_format, mid_format, low_format]
            
            format_list = []
            for f in selected_formats:
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                format_note = f.get('format_note', 'N/A')
                filesize = f.get('filesize', 'Unknown size')
                format_str = f"{ext} - {format_note} - {filesize}"
                format_list.append({'id': format_id, 'description': format_str})
            
            return format_list, thumbnail
    except yt_dlp.DownloadError as e:
        print(f"Error listing formats: {e}")
        return [], ''

def download_video(url, format_id, output_dir):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    video_file = os.path.join(output_dir, f'{timestamp}.mp4')
    final_file = os.path.join(output_dir, f'{timestamp}_final.mp4')

    ydl_opts_video = {
        'format': f'{format_id}+bestaudio',
        'outtmpl': video_file,
        'merge_output_format': 'mp4', 
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'ffmpeg_location': r'D:\influencer\ffmpeg-7.0.1-essentials_build\bin',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])
        if os.path.exists(video_file):
            os.rename(video_file, final_file)
        return final_file
    except yt_dlp.DownloadError as e:
        print(f"Error downloading video: {e}")
        return None

def index(request):
    fot = FooterDetail.objects.all()
    seo1 = Seo_Content.objects.all()
    seo = Seo_Settings.objects.select_related('page').all()

    if request.method == 'POST':
        url = request.POST['url']
        format_list, thumbnail = list_formats(url)
        if format_list:
            return render(request, 'twitterdownloader/formats.html', {'formats': format_list, 'url': url, 'thumbnail': thumbnail, "footer": fot, "Seo1": seo, "Seo": seo1})
        else:
            return HttpResponse("Failed to retrieve video formats.", status=500)
    return render(request, 'twitterdownloader/index.html', {"footer": fot, "Seo1": seo, "Seo": seo1})

def download_selected_view(request):
    if request.method == 'POST':
        url = request.POST['url']
        format_id = request.POST['format_id']
        output_dir = settings.TWITTER_DOWNLOAD_DIR
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
    return redirect('twitterdownloader:index')
