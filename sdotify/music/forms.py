from django import forms
from .models import Artist, Album, Song

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['artistName']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['albumName']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['songName']
