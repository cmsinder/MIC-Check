import json
import requests

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