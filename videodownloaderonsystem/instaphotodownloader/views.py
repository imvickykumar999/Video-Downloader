import os
import time
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse

def get_instagram_photo_url(instagram_url):
    """Extract the direct photo URL from the Instagram post URL."""
    response = requests.get(instagram_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tag = soup.find('meta', property='og:image')
        if meta_tag:
            return meta_tag['content']
    return None

def download_instagram_photo(photo_url, output_dir):
    """Download the photo from the given photo URL."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    photo_path = os.path.join(output_dir, f'{timestamp}.jpg')

    response = requests.get(photo_url)
    if response.status_code == 200:
        with open(photo_path, 'wb') as file:
            file.write(response.content)
        return photo_path
    return None

def index(request):
    if request.method == 'POST':
        url = request.POST['url']
        output_dir = settings.INSTAPHOTO_DOWNLOAD_DIR  # Use the new directory for instaphotodownloader
        os.makedirs(output_dir, exist_ok=True)
        photo_url = get_instagram_photo_url(url)
        if photo_url:
            photo_path = download_instagram_photo(photo_url, output_dir)
            if photo_path:
                photo_url = os.path.join(settings.MEDIA_URL, os.path.basename(photo_path))
                return render(request, 'instaphotodownloader/download.html', {'photo_url': photo_url})
        return HttpResponse("Failed to retrieve photo.", status=500)
    return render(request, 'instaphotodownloader/index.html')
