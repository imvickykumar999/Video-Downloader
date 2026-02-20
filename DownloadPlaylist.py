import yt_dlp
import os

def download_with_compatible_audio(playlist_url):
    download_path = 'StephenHawkingUniverse'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        # This force-sorts for mp4 video and m4a (AAC) audio
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{download_path}/%(playlist_index)s - %(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        # Post-processor to ensure audio is converted if it's not AAC
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    URL = "https://www.youtube.com/playlist?list=PL3A56CF555622FD46"
    download_with_compatible_audio(URL)
