from django.shortcuts import render, get_object_or_404
import requests
from googleapiclient.discovery import build
from ..models import Song

from ..models import Video
from django.conf import settings

def get_youtube_video(video_id):
    youtube = build('youtube', 'v3', developerKey='AIzaSyDTIlbQ46Z5900AgyhR0EE3-c-zV_XyqTc')
    response = youtube.videos().list(part='snippet', id=video_id).execute()
    if 'items' in response:
        video = response['items'][0]
        return video
    return None

def mv(request, song_id):
    video_data = get_object_or_404(Video, song_id=song_id)
    return render(request, 'music/mv.html', {'video': video_data})

def extract_video_id(video_url):
    # Lấy video ID từ URL, ví dụ: 'https://www.youtube.com/watch?v=VIDEO_ID'
    return video_url.split('v=')[-1]