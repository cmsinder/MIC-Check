import json
import requests
from bs4 import BeautifulSoup
import sqlite3
import os


path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'Movies Data Base.db')
cur = conn.cursor()


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

# tmdb_details_url = "https://api.themoviedb.org/3/movie/{}?api_key=773f87a98c4a4962613a1c61319b7edd&language=en-US"  # Ask about how this works or if it counts. Could I do {movie_id} and then set a parameter to change that?



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

#print('Printing title and release date: ')

#print(l_of_title_release_tups)

#print('Printing title and ids: ')

#print(l_of_title_id_tups)

#print('Printing title and scores: ')

#print(l_of_title_score_tups)

#print('Printing title and ratings: ')

#print(l_of_title_rating_tups)

#print('Printing title and box office: ')

#print(l_of_title_boxoffice_tups)



###   Calendar API gives list of public holidays. Country needs to be specified, so I'm doing US, but should we change the box office to only get domestic as well?   ###

calendar_url = "https://calendarific.com/api/v2/json"
l_of_title_holiday_tups = []
l_of_title_hnames_tups = []


for mov in l_of_title_release_tups:
    date_split = mov[1].split('-')  # Date is in the form of 'year-mo-da', so splitting it makes that a list to be indexed from
    calendar_params = {'api_key': '389c950ba1a94b1523ea48ee8ade9820b50815ac', 'country': 'US', 'year': int(date_split[0]), 'type': 'national', 'day': int(date_split[2]), 'month': int(date_split[1])}

    calendar_r = requests.get(calendar_url, calendar_params)
    calendar_data = calendar_r.json()

    if len(calendar_data['response']['holidays']) > 0:
        is_holiday = True

        for holiday in calendar_data['response']['holidays']:
            holdiay_name = holiday['name']
    else:
        is_holiday = False
        holdiay_name = 'N/A'

    title_holiday_tup = (mov[0], is_holiday)
    l_of_title_holiday_tups.append(title_holiday_tup)

    title_hname_tup = (mov[0], holdiay_name)
    l_of_title_hnames_tups.append(title_hname_tup)

cur.execute("CREATE TABLE IF NOT EXISTS TitleAndReleaseDate (title TEXT PRIMARY KEY, date TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS TitleAndID (title TEXT PRIMARY KEY, tmdbID INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS TitleAndScore (title TEXT PRIMARY KEY, score INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS TitleAndRatings (title TEXT PRIMARY KEY, rating TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS TitleAndBoxOffice (title TEXT PRIMARY KEY, boxoffice INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS TitleAndHoliday (title TEXT PRIMARY KEY, holiday BIT)")
cur.execute("CREATE TABLE IF NOT EXISTS TitleAndHolidayName (title TEXT PRIMARY KEY, holidayname TEXT)")

cur.executemany('INSERT INTO TitleAndReleaseDate (title, date) VALUES (?, ?)', l_of_title_release_tups)
cur.executemany('INSERT INTO TitleAndID (title, tmdbID) VALUES (?, ?)', l_of_title_id_tups)
cur.executemany('INSERT INTO TitleAndScore (title, score) VALUES (?, ?)', l_of_title_score_tups)
cur.executemany('INSERT INTO TitleAndRatings (title, rating) VALUES (?, ?)', l_of_title_rating_tups)
cur.executemany('INSERT INTO TitleAndBoxOffice (title, boxoffice) VALUES (?, ?)', l_of_title_boxoffice_tups)
cur.executemany('INSERT INTO TitleAndHoliday (title, holiday) VALUES (?, ?)', l_of_title_holiday_tups)
cur.executemany('INSERT INTO TitleAndHolidayName (title, holidayname) VALUES (?, ?)', l_of_title_hnames_tups)

conn.commit()