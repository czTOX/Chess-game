import tkinter as tk
import os
menu = tk.Tk()
menu.geometry('400x600')
menu.title('Šachy')


def single():
    os.startfile('chess.py')


def multi():
    os.startfile('chess.py')

# TODO fce buttonu, grafika menu, tlacitko na nej skore


nadpis = tk.Label(menu, text='Šachy')
nadpis.pack()
button_single = tk.Button(menu, text='Hra pro 1 hráče', command=single)
button_single.pack()
button_multi = tk.Button(menu, text='Hra pro 2 hráče', command=multi)
button_multi.pack()
button_help = tk.Button(menu, text='Nápověda')

menu.mainloop()