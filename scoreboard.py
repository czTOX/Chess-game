import tkinter as tk
import math
import ctypes
import os


file = open('zebricek.txt', 'r')
if os.stat("zebricek.txt").st_size != 0:
    scoreboard = tk.Tk()
    scoreboard.geometry('400x600')
    scoreboard.title('Scoreboard')
    for line in file:
        s = line.split(';')
        time = ("%02d:%02d" % (math.floor(float(s[2]))/60, math.floor(float(s[2])) % 60))
        text = s[0] + " porazil/a " + s[1] + " v čase: " + time
        label = tk.Label(scoreboard, text=text).pack()
    scoreboard.mainloop()
else:
    ctypes.windll.user32.MessageBoxW(0, 'Zatím není ve výsledcích ani jedna hra :(', 'File is empty', 1)
