from django.urls import path
from . import views

app_name = "recommender"
urlpatterns = [
    path('', views.index, name='index'),
    path('song_info/<str:track_id>/', views.song_info, name='song_info'),
]