import json
import requests
from bs4 import BeautifulSoup



l_of_movie_tups = []

###   TMDB Popular gives us a bunch of popular movies   ###

tmdb_url = "https://api.themoviedb.org/3/movie/popular?api_key=773f87a98c4a4962613a1c61319b7edd&language=en-US&"
tmdb_params = {'page':'1'}      # Need to change page number each time we run. Will run from 1-6 pages.

tmdb_r = requests.get(url = tmdb_url, params = tmdb_params)
tmdb_data = tmdb_r.json()

l_of_mov_titles = []
l_of_title_release_tups = []
l_of_title_id_tups = []

for movie in tmdb_data['results']:
    m_title = movie['title']
    l_of_mov_titles.append(m_title)
    
    m_release = movie['release_date']
    title_release_tup = (m_title, m_release)
    l_of_title_release_tups.append(title_release_tup)   # Create a table of titles and release dates

    m_tmbdid = movie['id']
    title_id_tup = (m_title, m_tmbdid)
    l_of_title_id_tups.append(title_id_tup)     # Create a table of titles and their TMDB ids, to be used in the other TMDB API



###   TMDB Details provides information on movies, takes TMDBid as input  ###

tmdb_details_url = "https://api.themoviedb.org/3/movie/{}?api_key=773f87a98c4a4962613a1c61319b7edd&language=en-US"  # Ask about how this works or if it counts. Could I do {movie_id} and then set a parameter to change that?



###   OMDB Takes list of movies and returns their title, score, rating, and imdbid ###

omdb_url = "http://www.omdbapi.com/?apikey=357b9dcf&"

l_of_title_score_tups = []
l_of_title_rating_tups = []
l_of_title_boxoffice_tups = []

for mov in l_of_mov_titles:
    omdb_params = {'t':mov}

    omdb_r = requests.get(url = omdb_url, params = omdb_params)
    omdb_data = omdb_r.json()
    
    if omdb_data['Response'] == 'True':
        mov_name = omdb_data['Title']
        for rate in omdb_data['Ratings']:
            if rate['Source'] == 'Rotten Tomatoes':
                mov_score = int(rate['Value'].strip('%'))
        mov_rating = omdb_data['Rated']
        mov_imdbid = omdb_data['imdbID']
    


###   Take mov_imdbid and put into Box Office Mojo    ###

        bom_url = "https://www.boxofficemojo.com/title/{}/?ref_=bo_se_r_1".format(mov_imdbid)
        soup = BeautifulSoup(requests.get(bom_url).text, 'html.parser')
        sum_tab = soup.find('div', class_ = "a-section a-spacing-none mojo-performance-summary-table")
        sum_tab_divs = sum_tab.find_all('div', class_ = "a-section a-spacing-none")
        for divs in sum_tab_divs:
            if 'Worldwide' in divs.find('span', class_ = "a-size-small").text:
                if divs.find('span', class_ = "money"):
                    mov_box = int(divs.find('span', class_ = "money").text.strip('$').replace(',', ''))
                else:
                    mov_box = 'N/A'

        title_score_tup = (mov_name, mov_score)
        l_of_title_score_tups.append(title_score_tup)
        
        title_rating_tup = (mov_name, mov_rating)
        l_of_title_rating_tups.append(title_rating_tup)
        
        title_boxoffice_tup = (mov_name, mov_box)
        l_of_title_boxoffice_tups.append(title_boxoffice_tup)

        # mov_tup = (mov_name, mov_rating, mov_score, mov_box)
        # l_of_movie_tups.append(mov_tup)

print('Printing title and release date: ')

print(l_of_title_release_tups)

print('Printing title and ids: ')

print(l_of_title_id_tups)

print('Printing title and scores: ')

print(l_of_title_score_tups)

print('Printing title and ratings: ')

print(l_of_title_rating_tups)

print('Printing title and box office: ')

print(l_of_title_boxoffice_tups)