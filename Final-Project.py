import json
import requests


###   TMDB Gives us a bunch of popular movies   ###

TMDB_url = "https://api.themoviedb.org/3/movie/popular?api_key=773f87a98c4a4962613a1c61319b7edd&language=en-US&"
TMDB_params = {'page':'1'}

TMDB_r = requests.get(url = TMDB_url, params = TMDB_params)
TMDB_data = TMDB_r.json()

l_of_movs = []

for movie in TMDB_data['results']:
    m_title = movie['title']
    l_of_movs.append(m_title)





###   OMDB Takes list of movies and returns tuple of (Title, Score, Box Office) ###

OMDB_url = "http://www.omdbapi.com/?apikey=357b9dcf&"

for mov in l_of_movs:
    OMDB_params = {'t':mov}

    OMDB_r = requests.get(url = OMDB_url, params = OMDB_params)
    OMDB_data = OMDB_r.json()
    
    mov_name = OMDB_data['Title']
    for rate in OMDB_data['Ratings']:
        if rate['Source'] == 'Rotten Tomatoes':
            mov_score = rate['Value']
    mov_box = OMDB_data['BoxOffice']
    mov_tup = (mov_name, mov_score, mov_box)
    print(mov_tup)