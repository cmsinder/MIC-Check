import json
import requests
from bs4 import BeautifulSoup

###   TMDB Gives us a bunch of popular movies   ###

tmdb_url = "https://api.themoviedb.org/3/movie/popular?api_key=773f87a98c4a4962613a1c61319b7edd&language=en-US&"
tmdb_params = {'page':'1'}

tmdb_r = requests.get(url = tmdb_url, params = tmdb_params)
tmdb_data = tmdb_r.json()

l_of_movs = []

for movie in tmdb_data['results']:
    m_title = movie['title']
    l_of_movs.append(m_title)





###   OMDB Takes list of movies and returns tuple of (Title, Score) ###

omdb_url = "http://www.omdbapi.com/?apikey=357b9dcf&"

for mov in l_of_movs:
    omdb_params = {'t':mov}

    omdb_r = requests.get(url = omdb_url, params = omdb_params)
    omdb_data = omdb_r.json()
    
    if omdb_data['Response'] == 'True':
        mov_name = omdb_data['Title']
        for rate in omdb_data['Ratings']:
            if rate['Source'] == 'Rotten Tomatoes':
                mov_score = rate['Value']
        mov_imdbid = omdb_data['imdbID']


###   Take mov_imdbid and put into Box Office Mojo    ###

    bom_url = "https://www.boxofficemojo.com/title/{}/?ref_=bo_se_r_1".format(mov_imdbid)
    soup = BeautifulSoup(requests.get(bom_url).text, 'html.parser')
    sum_tab = soup.find('div', class_ = "a-section a-spacing-none mojo-performance-summary-table")
    sum_tab_divs = sum_tab.find_all('div', class_ = "a-section a-spacing-none")
    for divs in sum_tab_divs:
        if 'Worldwide' in divs.find('span', class_ = "a-size-small").text:
            if divs.find('span', class_ = "money"):
                mov_box = divs.find('span', class_ = "money").text
            else:
                mov_box = "N/A"



    mov_tup = (mov_name, mov_score, mov_box)
    print(mov_tup)