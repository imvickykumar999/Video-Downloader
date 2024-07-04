from django.shortcuts import render
from django.conf import settings
import os

def list_video_folders(base_dir='downloaded_videos'):
    try:
        return [folder for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]
    except FileNotFoundError:
        return []

def home_view(request):
    video_folders = list_video_folders()
    videos = {}
    
    for folder in video_folders:
        folder_path = os.path.join(settings.MEDIA_ROOT, folder)
        if os.path.exists(folder_path):
            videos[folder] = [
                (file, os.path.join(settings.MEDIA_URL, folder, file))
                for file in os.listdir(folder_path) if file.endswith(('.mp4', '.mkv', '.webm'))
            ]
    
    return render(request, 'home.html', {'videos': videos})
