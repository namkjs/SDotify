from django.shortcuts import get_object_or_404, redirect
from ..models import Song, Playlist
from django.shortcuts import render
from home.models import User


def add_to_playlist_view(request, user_id, song_id):
    song = get_object_or_404(Song, pk=song_id)
    user = get_object_or_404(User, pk=user_id)  # Get user using user_id
    
    if request.method == 'POST':
        playlist, created = Playlist.objects.get_or_create(user=user)  # Get or create user's playlist
        playlist.songs.add(song)  # Add song to user's playlist if not already present
        playlist.save()
    return redirect('home')  # Redirect after successfully adding song to playlist



def show_music(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    return render(request, 'music/showplaylist.html', {'playlists': playlist})
