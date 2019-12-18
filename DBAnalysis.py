import sqlite3
import os
import statistics
import matplotlib
import matplotlib.pyplot as plt
matplotlib.axes.Axes.pie
matplotlib.pyplot.pie



path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'Movies Data Base.db')
cur = conn.cursor()


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
    elif y == 'holidayname':
        y_table_title = 'TitleAndHolidayName'


    cur.execute("SELECT {} FROM {}".format(x, x_table_title))
    for row in cur:
        k = row[0]
        if k not in dict_for_analysis:
            dict_for_analysis[k] = []
    
    cur.execute("SELECT {}, {} FROM {} LEFT JOIN {} ON {}.title = {}.title".format(x, y, x_table_title, y_table_title, x_table_title, y_table_title))

    for row in cur:
        for k in dict_for_analysis.keys():
            if row[0] == k:
                if row[1] == 'N/A':
                    continue
                else:
                    dict_for_analysis[k].append(row[1])
    
    return dict_for_analysis



###   Joining TitleAndRatings with TitleAndBoxOffice  ###

cur.execute("SELECT rating, boxoffice FROM TitleAndRatings LEFT JOIN TitleAndBoxOffice ON TitleAndRatings.title = TitleAndBoxOffice.title")


###   MATH    ###

dict_of_ratings = {'G': [], 'PG': [], 'PG-13': [], 'R': [] ,'N/A': [], 'Not Rated' : [],'TV-MA' : [],'TV-PG': [] }

for row in cur:
    if row[0] == 'N/A':
        continue
    elif row[0] == 'G':
        dict_of_ratings['G'].append(row[1])
    elif row[0] == 'PG':
        dict_of_ratings['PG'].append(row[1])
    elif row[0] == 'TV-PG':
        dict_of_ratings['TV-PG'].append(row[1])
    elif row[0] == 'PG-13':
        dict_of_ratings['PG-13'].append(row[1])
    elif row[0] == 'R':
        dict_of_ratings['R'].append(row[1])
    elif row[0] == 'N/A':
        dict_of_ratings['N/A'].append(row[1])
    elif row[0] == 'Not Rated':
        dict_of_ratings['Not Rated'].append(row[1])
    elif row[0] == 'TV-MA':
        dict_of_ratings['TV-MA'].append(row[1])
 

#avg_G_bo = statistics.mean(dict_of_ratings['G'])
#avg_PG_bo = statistics.mean(dict_of_ratings['PG'])
#avg_PG13_bo = statistics.mean(dict_of_ratings['PG-13'])
#avg_R_bo = statistics.mean(dict_of_ratings['R'])


###   Writing calculations to a file  ###


root_path = os.path.dirname(os.path.abspath(__file__))
w_filename = root_path + '/' + "AverageBoxOfficeByRating.txt"
outfile = open(w_filename, 'w')

#for rating in dict_of_ratings.keys():
#    outfile.write("The average money earned at the Box Office for movies rated {} was: $".format(rating) + str(round(statistics.mean(dict_of_ratings[rating]))) + '\n')

outfile.close()




# print(calculate_from_db('rating', 'boxoffice'))




#VISUAL 1 creates bar chart of the movies, sorted by genre
rating_bo_dict = calculate_from_db('rating', 'boxoffice')
key1 = list(rating_bo_dict.keys())
val = []
for i in rating_bo_dict:
    len1 = len(rating_bo_dict[i])
    val.append(len1)

plt.bar(key1, val, color = ('green', 'blue', 'green', 'blue', 'green', 'blue', 'blue'))
plt.xlabel("Movie Ratings")
plt.ylabel("Quantity of Movies")
plt.title("Ratings Fragmentation of Top 100 Movies")
plt.tight_layout()
# print(rating_bo_dict)
# print(key1)
# print(val)
plt.show()



#VISUAL 2 scatterplot of average box office each year
year_bo_dict = calculate_from_db('year', 'boxoffice')
#print(year_bo_dict)
years = list(year_bo_dict.keys())
total = year_bo_dict.values()
avg_bo = []
for box in total:
    sum_bo = 0
    num = len(box)
    for i in box:
        sum_bo += i
        #print(i)
    avg = sum_bo/num
    avg_bo.append(avg)

plt.scatter(years, avg_bo, color = 'g')
plt.title("Gauging Average Box Office Growth Year-Over-Year")
plt.xlabel("Year")
plt.ylabel("Mean Box Office Revenue (in $Billions USD)")

plt.show()

#VISUAL 3 Scatterplot of average rating score by genre

rating_score_bo = calculate_from_db('rating' , 'score')
ratings = rating_score_bo.keys()
scores = rating_score_bo.values()
# print(rating_score_bo)

score_a = []
for list1 in scores:
    sums = 0
    len_score = len(list1)
    if len_score > 0:
        for i in list1:
            sums += i
        avg_ratingscore = sums/len_score
        score_a.append(avg_ratingscore)
    else:
        score_a.append(0)
        #need to adjust scores for N/A rating
    

plt.scatter(ratings, score_a, color = 'b')
plt.title("Average Top Movie User Scores by Rating")
plt.xlabel("Rating")
plt.ylabel("Average User-Given Score")

plt.show()


#VISUAL 4 PIE CHART Showing Segmentation of the Top 100 Movies by Genre

labels = 'PG', 'PG-13', 'R', 'G', 'N/A', 'Not Rated'
sizes = [16, 46, 27, 4, 3,2]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Percentage Segmentation of Top 100 Movies by Genre")


plt.show()

#VISUAL 5 BAR CHART illustrates the average box office by movie rating

boxgenr1 = calculate_from_db('genre', 'boxoffice')
#print(year_bo_dict)
genre = list(boxgenr1.keys())
total = boxgenr1.values()
avg_box = []

for i in total:
    sums = 0
    len_score = len(i)
    if len_score > 0:
        for x in i:
            sums += x
        avg_ = sums/len_score
        avg_box.append(avg_)
    else:
        avg_box.append(0)
print(avg_box)

plt.bar(genre, avg_box, color = ('green', 'blue', 'green', 'blue', 'green', 'blue', 'blue'))
plt.xlabel("Genre")
plt.ylabel("Mean Box Office Across Genre in $Billion USD")
plt.title("Average Box Office by Genre for Top 100 Movies From List")
plt.tight_layout()

plt.show()

