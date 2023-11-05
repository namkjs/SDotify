from django.shortcuts import render
import requests
from googleapiclient.discovery import build

from ..models import Video
from django.conf import settings

def get_youtube_video(video_id):
    youtube = build('youtube', 'v3', developerKey='AIzaSyDTIlbQ46Z5900AgyhR0EE3-c-zV_XyqTc')
    response = youtube.videos().list(part='snippet', id=video_id).execute()
    if 'items' in response:
        video = response['items'][0]
        return video
    return None

def mv(request):
    if request.method == 'POST':
        video_url = request.POST['video_url']
        video_id = extract_video_id(video_url)
        video_data = get_youtube_video(video_id)
        if video_data:
            video, created = Video.objects.get_or_create(
                video_id=video_id,
                defaults={
                    'title': video_data['snippet']['title'],
                    'published_date': video_data['snippet']['publishedAt']
                }
            )
        return render(request, 'music/mv.html', {'video': video_data})
    return render(request, 'music/mv.html')

def extract_video_id(video_url):
    # Lấy video ID từ URL, ví dụ: 'https://www.youtube.com/watch?v=VIDEO_ID'
    return video_url.split('v=')[-1]