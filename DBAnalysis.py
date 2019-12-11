import sqlite3
import os
import statistics

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'Movies Data Base.db')
cur = conn.cursor()

###   Joining TitleAndRatings with TitleAndBoxOffice  ###

cur.execute("SELECT rating, boxoffice FROM TitleAndRatings LEFT JOIN TitleAndBoxOffice ON TitleAndRatings.title = TitleAndBoxOffice.title")


###   MATH    ###

dict_of_ratings = {'G': [], 'PG': [], 'PG-13': [], 'R': []}

for row in cur:
    if row[0] == 'N/A':
        continue
    elif row[0] == 'G':
        dict_of_ratings['G'].append(row[1])
    elif row[0] == 'PG':
        dict_of_ratings['PG'].append(row[1])
    elif row[0] == 'PG-13':
        dict_of_ratings['PG-13'].append(row[1])
    elif row[0] == 'R':
        dict_of_ratings['R'].append(row[1])


avg_G_bo = statistics.mean(dict_of_ratings['G'])
avg_PG_bo = statistics.mean(dict_of_ratings['PG'])
avg_PG13_bo = statistics.mean(dict_of_ratings['PG-13'])
avg_R_bo = statistics.mean(dict_of_ratings['R'])


###   Writing calculations to a file  ###


root_path = os.path.dirname(os.path.abspath(__file__))
w_filename = root_path + '/' + "AverageBoxOfficeByRating.txt"
outfile = open(w_filename, 'w')

for rating in dict_of_ratings.keys():
    outfile.write("The average money earned at the Box Office for movies rated {} was: $".format(rating) + str(round(statistics.mean(dict_of_ratings[rating]))) + '\n')

outfile.close()


###   Defining a function that should make calculations easy  ###


def calculate_from_db(x, y):
    dict_for_analysis = {}

    if x == 'year':     # Set up a way to get each table. Repeat with y.
        x_table_title = 'TitleAndReleaseYear'
    elif x == 'genre':
        x_table_title = 'TitleAndGenre'
    elif x == 'score':
        x_table_title = 'TitleAndScore'
    elif x == 'rating':
        x_table_title = 'TitleAndRatings'
    elif x == 'boxoffice':
        x_table_title = 'TitleAndBoxOffice'
    elif x == 'holiday':
        x_table_title = 'TitleAndHoliday'
    elif x == 'holidayname':
        x_table_title = 'TitleAndHolidayName'


    if y == 'year':     # Set up a way to get each table. Repeat with y.
        y_table_title = 'TitleAndReleaseYear'
    elif y == 'genre':
        y_table_title = 'TitleAndGenre'
    elif y == 'score':
        y_table_title = 'TitleAndScore'
    elif y == 'rating':
        y_table_title = 'TitleAndRatings'
    elif y == 'boxoffice':
        y_table_title = 'TitleAndBoxOffice'
    elif y == 'holiday':
        y_table_title = 'TitleAndHoliday'
    elif y == 'holidayname'
        y_table_title = 'TitleAndHolidayName'


    cur.execute("SELECT {} FROM {}".format(x, x_table_title))
    for row in cur:
        if row not in dict_for_analysis:
            dict_for_analysis[row] = []
    
    cur.execute("SELECT {}, {} FROM {} LEFT JOIN {} ON {}.title = {}.title".format(x, y, x_table_title, y_table_title, x_table_title, y_table_title))

    for row in cur:
        for k in dict_for_analysis.keys():
            if row[0] == k:
                dict_for_analysis[k].append(row[1])
    
    return dict_for_analysis
