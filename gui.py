import tkinter as tk
import sqlite3
import datetime
import RPi.GPIO as GPIO

database = 'PartVibeTime.db'
after_id = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)


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
        return(timer[0])
    else:
        error.configure(text='Part not found')
        return(0)


def stopMachine():
    GPIO.output(18, GPIO.LOW)
    global after_id
    if after_id:
        window.after_cancel(after_id)
        after_id = None
    vibeTimer.configure(text=0)
    status.configure(text="Off")
    error.configure(text="None")


def countdown(remaining):
    global after_id
    if remaining > 0:
        GPIO.output(18, GPIO.HIGH)
        vibeTimer.configure(text=str(datetime.timedelta(seconds=remaining)))
        after_id = window.after(1000, countdown, remaining-1)
    else:
        stopMachine()


def startMachine(timer):
    timerText = timer, 'min'
    vibeTimer.configure(text=timerText)
    status.configure(text="Running")
    error.configure(text="None")
    countdown(timer)


def submitPart(event=None):
    part = text.get()
    timer = getVibeTime(part)
    if timer != 0:
        startMachine(timer)


window = tk.Tk()
window.title("Vibe Control Timer")
window.geometry('480x320')
window.option_add("*Font", "courier 14")
prompt = tk.Label(window, text="Enter Part#:")
prompt.grid(column=0, row=0)
text = tk.Entry(window, width=15)
text.focus()
text.grid(column=1, row=0)
start = tk.Button(window, text="Start", command=submitPart)
window.bind('<Return>', submitPart)
start.grid(column=2, row=0)
statusLabel = tk.Label(window, text="Machine Status: ")
statusLabel.grid(column=0, row=1)
status = tk.Label(window, text="Off")
status.grid(column=1, row=1)
timeLabel = tk.Label(window, text="Vibe Time")
timeLabel.grid(column=0, row=2)
vibeTimer = tk.Label(window, text="0")
vibeTimer.grid(column=1, row=2)
errorLable = tk.Label(window, text="Error:")
errorLable.grid(column=0, row=3)
error = tk.Label(window, text="None")
error.grid(column=1, row=3)
stopButton = tk.Button(window, text='Stop!', command=stopMachine)
stopButton.grid(column=2, row=3)
window.mainloop()
