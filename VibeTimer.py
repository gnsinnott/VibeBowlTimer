import sqlite3
from datetime import datetime
import time


# TO DO
# ADD ALARM WHEN COMPLETE?
# USE BARCODE AND SCANNER TO ENTER PART NUMBER
# USE BARCODE FOR VIBE CLEARING PROCESS OR ALTERNATIVE METHOD?


# Create connection to database
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


# Create Record of activity in Database
def createRecord(part, conn, vibeTimer):
    sql = '''INSERT INTO Activity(Part, Time, VibeTime) VALUES (?,?,?)'''
    cur = conn.cursor()
    currentTime = datetime.now()
    cur.execute(sql, (part, currentTime, vibeTimer))
    conn.commit()
    return(0)


# Used to run vibe for short period of time to remove all parts
def clearVibe():
    while True:
        entry = input('Enter 0 for 30sec, 1 for 60sec of '
                      'additional vibe time or * to end: ')
        if entry == '*':
            print('\n')
            break
        if entry == '0':
            additionalVibe = 3
            startTimer(additionalVibe)
        if entry == '1':
            additionalVibe = 6
            startTimer(additionalVibe)
        else:
            print('Invalid entry, try again.')
    main()


# Begin timer
def startTimer(vibeTimer):
    print(f'Vibe Time is {vibeTimer} seconds.')
    print('Vibe Start')
    time.sleep(vibeTimer)
    print('Vibe Complete')
    clearVibe()


# Get vibe time from database per Part #
def getVibeTime(conn):
    sql = '''SELECT Time from PartVibeTime where Part =?'''
    part = input("What part number are you processing?")
    cur = conn.cursor()
    cur.execute(sql, (part,))
    timer = cur.fetchone()
    if timer is not None:
        return(timer[0], part)
    else:
        print('Not a valid part')
        main()


# Collect part number
def main():
    database = "PartVibeTime.db"
    conn = create_connection(database)
    vibeTimer, part = getVibeTime(conn)
    createRecord(part, conn, vibeTimer)
    print("Entry made.")
    startTimer(vibeTimer)


if __name__ == "__main__":
    main()
