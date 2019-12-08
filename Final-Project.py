import json
import requests


###   TMDB Gives us a bunch of popular movies   ###

url = "https://api.themoviedb.org/3/movie/popular?api_key=773f87a98c4a4962613a1c61319b7edd&language=en-US&"
params = {'page':'1'}

r = requests.get(url = url, params = params)
data = r.json()

l_of_movs = []

for movie in data['results']:
    m_title = movie['title']
    l_of_movs.append(m_title)

print(l_of_movs)
print(len(l_of_movs))



###   OMDB Takes list of movies and returns tuple of (Title, Score, Box Office) ###

url = "http://www.omdbapi.com/?apikey=357b9dcf&"

for mov in mov_list:
    params = {'t':mov}

    r = requests.get(url = url, params = params)
    data = r.json()
    
    mov_name = data['Title']
    for rate in data['Ratings']:
        if rate['Source'] == 'Rotten Tomatoes':
            mov_score = rate['Value']
    mov_box = data['BoxOffice']
    mov_tup = (mov_name, mov_score, mov_box)
    print(mov_tup)