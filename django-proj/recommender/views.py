from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd


df = pd.read_csv('recommender/spotify_tracks_clustered_exported.csv')
def search_song(song_name):
    if not isinstance(song_name, str):
        raise ValueError(type(song_name))
    simlar_song = df[df['track_name'].str.contains(song_name, case=False) | df['artist_name'].str.contains(song_name, case=False)]
    return simlar_song

def track_song(track_id):
    if not isinstance(track_id, str):
        raise ValueError(type(track_id))
    song = df[df['track_id'] == track_id]
    return song

def recommend_song(track_id):
    if not isinstance(track_id, str):
        raise ValueError(type(track_id))
    song = df[df['track_id'] == track_id]
    cluster = song['Cluster'].values[0]
    language = song['language'].values[0]
    genre = song['genre'].values[0]
    recommend_songs = df.loc[(df['genre'] == genre) & (df['language'] == language) & (df['Cluster'] == cluster)]
    recommended_songs = recommend_songs[recommend_songs['track_id'] != track_id].sort_values(by='popularity', ascending=False)
    return recommended_songs[:5]

# Create your views here.
def index(request):
    similar_song = None
    if request.method == 'POST':
        song_name = request.POST.get('song_name')
        similar_song = search_song(song_name)
    template = loader.get_template('recommender/index.html')
    context = {
        'similar_song': similar_song.to_dict('records') if similar_song is not None else None
    }
        # do something with the POST data
    return HttpResponse(template.render(context, request))

def song_info(request, track_id):
    template = loader.get_template('recommender/song_info.html')
    song_details = track_song(track_id)
    recommended_songs = recommend_song(track_id)
    context = {
        'track_id': track_id,
        'song_details': song_details.to_dict('records'),
        'recommended_songs': recommended_songs.to_dict('records')
    }
    return HttpResponse(template.render(context, request))
