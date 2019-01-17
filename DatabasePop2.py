import csv, sqlite3

con = sqlite3.connect("PartVibeTime.db")
cur = con.cursor()

with open('A2Times.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['Part'], i['Time'], i['Cans']) for i in dr]

cur.executemany("INSERT INTO PartVibeTime (Part, Time, Cans) VALUES (?, ?, ?);", to_db)
con.commit()
con.close()