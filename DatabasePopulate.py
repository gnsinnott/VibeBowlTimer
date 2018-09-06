import sqlite3
import csv


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def CreateRecords(vibeDict, conn):
    sql = '''INSERT INTO PartVibeTime(Part, Time) VALUES (?,?)'''
    cur = conn.cursor()
    for key, value in vibeDict.items():
        part = key
        time = value
        cur.execute(sql, (part, time))
        conn.commit()


def CSVtoDict(file):
    with open('vibe.csv', mode='r') as infile:
        reader = csv.reader(infile)
        with open('vibe_new.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            mydict = {rows[0]: rows[1] for rows in reader}
            print(mydict)
    return mydict


def main():
    database = "PartVibeTime.db"
    csvfile = "vibe.csv"
    conn = create_connection(database)
    mydict = CSVtoDict(csvfile)
    CreateRecords(mydict, conn)


if __name__ == "__main__":
    main()
