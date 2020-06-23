#!/usr/bin/python3
from tkinter import Tk, Label, Button
import os

class launcherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Vibe Bowl Launcher")

        self.label = Label(master, text="Select an Application")
        self.label.pack(fill='x')

        self.controller_button = Button(master, text="Start Vibe Controller", command=self.launchController)
        self.controller_button.pack(fill='x', pady=5)

        self.database_button = Button(master, text="Modify Database", command=self.launchDatabaseModifier)
        self.database_button.pack(fill='x')

    def launchController(self):
        print("Launch Vibe Controller GUI")
        self.master.destroy()
        os.system('python3 gui.py')

    def launchDatabaseModifier(self):
        print("Launch Database Modifier GUI")
        self.master.destroy()
        os.system('python3 DatabaseModifierGUI.py')

root = Tk()
my_gui = launcherGUI(root)
root.mainloop()
