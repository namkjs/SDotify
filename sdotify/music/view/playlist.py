from django.shortcuts import get_object_or_404, redirect
from ..models import Song, Playlist
from django.shortcuts import render

def add_to_playlist_view(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.method == 'POST':
        # Lấy hoặc tạo danh sách phát của người dùng (ở đây mình giả sử user_id = 1)
        user_id = 1  # Bạn cần thay đổi để lấy user_id từ request hoặc thông tin đăng nhập
        playlist, created = Playlist.objects.get_or_create(user_id=user_id, playlistName='Default Playlist')

        # Thêm bài hát vào danh sách phát của người dùng nếu chưa có
        playlist.songs.add(song)

    return redirect('home')  # Chuyển hướng sau khi thêm bài hát vào danh sách phát thành công

def show_playlists(request):
    user_id = request.user.id

    playlists = Playlist.objects.filter(user_id=user_id)
    return render(request, 'music/playlist.html', {'playlists': playlists})



def create_new_playlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            new_playlist_name = request.POST.get('new_playlist_name')
            # Tạo playlist mới và thêm bài hát vào playlist đó
            playlist = Playlist.objects.create(user=request.user, playlistName=new_playlist_name)

            # Chuyển hướng về trang hoặc URL mong muốn sau khi tạo playlist thành công
            return redirect('home')
        else:
            # Xử lý khi người dùng không đăng nhập
            # Ví dụ: chuyển hướng người dùng đến trang đăng nhập
            return redirect('login')

    # Nếu request không phải là POST, có thể thực hiện các xử lý khác nếu cần
    return render(request, 'music/playlist.html')

