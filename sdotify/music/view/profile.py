from django.shortcuts import render, get_object_or_404
from ..models import Artist

def artist_profile(request, artist_name):
    artist = get_object_or_404(Artist, artistName=artist_name)
    return render(request, 'music/artist_profile.html', {'artist': artist})
