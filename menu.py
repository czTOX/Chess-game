import tkinter as tk
from funkce import name_tab


menu = tk.Tk()
menu.geometry('400x600')
menu.title('Šachy')


def single():
    menu.destroy()
    name_tab(1)
    # TODO zadaní jmen
    import ai


def multi():
    menu.destroy()
    name_tab(0)
    # TODO zadaní jmena
    import chess


def score():
    import scoreboard


def guide():
    # TODO napověda
    pass


nadpis = tk.Label(menu, text='Šachy')
nadpis.pack()
button_single = tk.Button(menu, text='Hra pro 1 hráče', command=single)
button_single.pack()
button_multi = tk.Button(menu, text='Hra pro 2 hráče', command=multi)
button_multi.pack()
button_help = tk.Button(menu, text='Nápověda', command=guide)
button_help.pack()
button_score = tk.Button(menu, text='Nejlepší výsledky', command=score)
button_score.pack()

menu.mainloop()