#!/usr/bin/python3
from tkinter import Tk, Label, Button, Text, Frame, messagebox, Entry
import sqlite3
from sqlite3 import Error


database = 'PartVibeTime.db'

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None

def getVibeTime(part):
    sql = '''SELECT Time from PartVibeTime where Part =?'''
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, (part,))
    timer = cur.fetchone()
    if timer is not None:
        vibeTime = timer[0]
        return(vibeTime)
    else:
        print("nothing found")
        return(0)

def changeVibeTime(part, newTime):
    data = (newTime, part)
    sql = '''UPDATE PartVibeTime set Time = ? where Part = ?'''
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

class DatabaseModifierGUI:
    def __init__(self, master):
        self.master = master
        master.title("Database Modifier")

        self.label = Label(master, text="Database Modifier")
        self.label.pack()

        partFrame = Frame(master)
        partFrame.pack()

        returnFrame = Frame()
        returnFrame.pack()

        updateFrame = Frame(master)
        updateFrame.pack()

        self.partPrompt = Label(partFrame, text="Enter Part #")
        self.partPrompt.pack(side="left")

        self.partEntry = Entry(partFrame)
        self.partEntry.pack(side="left")

        self.searchButton = Button(partFrame, text="Search", command=self.searchPart)
        self.searchButton.pack(side="left")

        self.currentTimePrompt = Label(returnFrame, text="Current Time:")
        self.currentTimePrompt.pack(side="left")

        self.currentTime = Label(returnFrame, text="     ")
        self.currentTime.pack(side="left")

        self.newTimePrompt = Label(updateFrame, text="New Time:")
        self.newTimePrompt.pack(side="left")

        self.newTimeEntry = Entry(updateFrame)
        self.newTimeEntry.pack(side="left")

        self.newTimeButton = Button(updateFrame, text="Submit", command=self.submitChange)
        self.newTimeButton.pack(side="left")

    def searchPart(self):
        part = self.partEntry.get()
        time = getVibeTime(part)
        print(time)
        self.currentTime.configure(text=time)
        print(part)

    def submitChange(self):
        part = self.partEntry.get()
        newTime = self.newTimeEntry.get()
        oldTime = self.currentTime.cget("text")
        changeMessage = "Do you want to change the vibe time from: %s to %s" %(oldTime, newTime)
        confirmMessage = messagebox.askquestion("Make Change", changeMessage)
        if confirmMessage == 'yes':
            changeVibeTime(part, newTime)
            root.destroy
            print("Change made")

        print(newTime)

root = Tk()
my_gui = DatabaseModifierGUI(root)
root.mainloop()
