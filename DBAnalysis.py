import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'Movies Data Base.db')
cur = conn.cursor()

###   Joining TitleAndRatings with TitleAndBoxOffice  ###

cur.execute("SELECT rating, boxoffice FROM TitleAndRatings LEFT JOIN TitleAndBoxOffice ON TitleAndRatings.title = TitleAndBoxOffice.title")





###   MATH    ###