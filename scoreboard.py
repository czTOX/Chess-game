import tkinter as tk
import math


scoreboard = tk.Tk()
scoreboard.geometry('400x600')
scoreboard.title('Scoreboard')

file = open('zebricek.txt', 'r')
for line in file:
    s = line.split(';')
    text = s[0] + " porazil/a " + s[1] + " v čase: " + ("%02d:%02d" % (math.floor(float(s[2]))/60, math.floor(float(s[2])) % 60))
    label = tk.Label(scoreboard, text=text).pack()

scoreboard.mainloop()
