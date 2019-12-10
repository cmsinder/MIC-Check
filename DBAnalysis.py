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
    if row[1] == 'N/A':
        continue
    if row[0] == 'G':
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