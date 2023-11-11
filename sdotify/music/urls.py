from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.index, name ='home'),
    path('search/', views.search_songs, name='search_songs'),
    path('artist/<str:artist_name>/', views.artist_profile, name='artist_profile'),
    path('mv/<int:song_id>/', views.mv, name = "mv" )
    # Các URL khác của app2 ở đây
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()