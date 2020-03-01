# Knihovny
import pygame
import tkinter as tk
import figurky
from variables import *
import math


# Třídy
class Button:
    def __init__(self, clr, x, y, width, height, text=''):
        self.color = clr
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('trebuchetms', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def over(self, pos):
        # pos[0] > self.x and pos[0] < self.x + self.width
        if self.x < pos[0] < self.x + self.width:
            # pos[1] > self.y and pos[1] < self.y + self.height
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


# Funkce
def vykresli_sachovnici(window, strana_sachovnice):
    is_black = False
    strana = strana_sachovnice/8
    for i in range(8):
        for j in range(8):
            if is_black:
                pygame.draw.rect(window, [196, 99, 38], (j * strana, i * strana, strana, strana))
            else:
                pygame.draw.rect(window, [253, 223, 179], (j * strana, i * strana, strana, strana))
            is_black = not is_black
        is_black = not is_black
    pygame.draw.line(window, [0, 0, 0], (strana_sachovnice, 0), (strana_sachovnice, strana_sachovnice), 3)


def vykresli_pole(window, pole):
    for i in pole:
        for item in i:
            if item is not '':
                item.draw(window)


def vyber():

    vyber_okno = tk.Tk()
    vyber_okno.geometry('300x300')
    vyber_okno.title('Výběr figurky')
    neco = tk.StringVar(value='Kralovna')

    def zavri():
        vyber_okno.destroy()

    nadpis = tk.Label(vyber_okno, text='Vyber figurku, kterou chceš svého pěšce nehradit:')
    nadpis.pack()
    b_kralovna = tk.Radiobutton(vyber_okno, text='kralovna', variable=neco, value='Kralovna')
    b_kralovna.pack()
    b_strelec = tk.Radiobutton(vyber_okno, text='strelec', variable=neco, value='Strelec')
    b_strelec.pack()
    b_kun = tk.Radiobutton(vyber_okno, text='kun', variable=neco, value='Kun')
    b_kun.pack()
    b_vez = tk.Radiobutton(vyber_okno, text='vez', variable=neco, value='Vez')
    b_vez.pack()
    submit = tk.Button(vyber_okno, text='Submit', command=zavri)
    submit.pack()

    vyber_okno.mainloop()

    return neco.get()


def vyresli_moznosti(window, sug):
    for each in sug:
        # pygame.draw.circle(window, [255, 20, 0], (each[0]*100+50, each[1]*100+50), 15)
        pygame.draw.rect(window, [7, 191, 64], (each[0]*100+2, each[1]*100+2, 96, 96), 3)


def refresh(widnow, pole):
    vykresli_sachovnici(widnow, 800)
    vykresli_pole(widnow, pole)
    pygame.display.update()


def vypis_mrtvych(window, dead):
    posun_black = 0
    posun_white = 0
    for item in dead:
        if item.jecerna:
            item.this = pygame.transform.scale(item.this, (25, 25))
            window.blit(item.this, (900+posun_black, 200))
            posun_black += 30
        else:
            item.this = pygame.transform.scale(item.this, (25, 25))
            window.blit(item.this, (900 + posun_white, 575))
            posun_white += 30


def zapis_skore(time):
    zebricek = open("zebricek.txt", "a+")
    zebricek.write(names[0] + ";" + names[1] + ";" + str(time) + "\n")
    zebricek.close()


def je_v_sachu(pole, souradnice, enemy_figs):
    for fig in enemy_figs:
        if type(fig) == figurky.Pesak:
            if fig.jecerna:
                if souradnice == [fig.x + 1, fig.y + 1] or souradnice == [fig.x - 1, fig.y + 1]:
                    return True
            else:
                if souradnice == [fig.x - 1, fig.y - 1] or souradnice == [fig.x + 1, fig.y - 1]:
                    return True
        elif type(fig) == figurky.Kral:
            if souradnice in fig.kam2(pole):
                return True
        elif souradnice in fig.kam(pole):
            return True
    return False


def block(pole, souradnice, friendly_figs, enemy_figs):
    for friend in friendly_figs:
        for place in friend.kam(pole):
            backup_coords = [friend.x, friend.y]
            recover_fig = ''
            if pole[place[0]][place[1]] is not '':
                recover_fig = pole[place[0]][place[1]]
                enemy_figs.remove(recover_fig)
            if type(friend) == figurky.Pesak or type(friend) == figurky.Kral:
                friend.move2(pole, [place[0], place[1]])
            else:
                friend.move(pole, [place[0], place[1]])

            if je_v_sachu(pole, souradnice, enemy_figs):
                if type(friend) == figurky.Kral:
                    friend.move2(pole, backup_coords)
                else:
                    friend.move(pole, backup_coords)
                pole[place[0]][place[1]] = recover_fig
                if recover_fig is not '':
                    enemy_figs.append(recover_fig)
            else:
                if type(friend) == figurky.Kral:
                    friend.move2(pole, backup_coords)
                else:
                    friend.move(pole, backup_coords)
                pole[place[0]][place[1]] = recover_fig
                if recover_fig is not '':
                    enemy_figs.append(recover_fig)
                return True
    return False


def je_mat(pole, souradnice, friendly_figs, enemy_figs):
    if je_v_sachu(pole, souradnice, enemy_figs):
        # Může se král movnou někam, kde by šach neměl
        if not pole[souradnice[0]][souradnice[1]].kam(pole):
            # Může šach nějaká figurka zablokovat nebo vyhodit figurku, která mu dává šach
            if not block(pole, souradnice, friendly_figs, enemy_figs):
                return True
    return False


def pat(pole, souradnice, friendly_figs, enemy_figs):
    if not je_v_sachu(pole, souradnice, enemy_figs):
        if not pole[souradnice[0]][souradnice[1]].kam(pole):
            if not block(pole, souradnice, friendly_figs, enemy_figs):
                return True
    return False


def name_tab(typ):
    def play():
        if textbox1.get() != '':
            names.append(textbox1.get())
        else:
            names.append('Player1')
        if textbox2.get() != '':
            names.append(textbox2.get())
        else:
            names.append('Player2')
        okno.destroy()

    def play2():
        if textbox1.get() != '':
            names.append(textbox1.get())
        else:
            names.append('Player1')
        names.append('AI')

        names.append(obtiznost)
        okno.destroy()

    okno = tk.Tk()
    okno.geometry('200x100')
    # Zadání 2 jmen pro multiplayer mód
    if typ == 0:
        okno.title('Zadejte jména hráčů')

        label1 = tk.Label(okno, text='Bílá:')
        label1.pack()
        textbox1 = tk.Entry(okno)
        textbox1.focus_set()
        textbox1.pack()
        label2 = tk.Label(okno, text='Černá:')
        label2.pack()
        textbox2 = tk.Entry(okno)
        textbox2.pack()
        button = tk.Button(okno, text='Hrát!', command=play)
        button.pack()

    # Zadání jména pro hru s AI
    elif typ == 1:
        okno.geometry('200x250')
        obtiznost = tk.IntVar()
        okno.title('Zadej jméno hráče')

        label1 = tk.Label(okno, text='Jméno:')
        label1.pack()
        textbox1 = tk.Entry(okno)
        textbox1.focus_set()
        textbox1.pack()
        lehke = tk.Radiobutton(okno, text='Lehká', variable=obtiznost, value=1)
        lehke.select()
        lehke.pack()
        stredni = tk.Radiobutton(okno, text='Střední', variable=obtiznost, value=2)
        stredni.pack()
        tezke = tk.Radiobutton(okno, text='Těžká', variable=obtiznost, value=3)
        tezke.pack()
        button = tk.Button(okno, text='Hrát!', command=play2)
        button.pack()

    okno.mainloop()


# ------------------- AI stuff ------------------- *
def minimax(pole, hloubka, ismax, alfa, beta):
    # Báze
    if hloubka == 1 or (stav(pole) != 0):
        a = stav(pole)
        if a == 0:
            return ohodnoceni(pole)
        elif a == 1:
            return 9999
        elif a == -1:
            return -9999
        elif a == 2:
            return 50
        elif a == -2:
            return -50

    # else:
    if ismax:           # Maximalizující tah
        hodnota = -math.inf
        for move in get_moves(pole, ismax):
            item = move[0]
            backup_coords = [item.x, item.y]
            recover_fig = pole[move[1]][move[2]]
            if recover_fig != '':
                if recover_fig.jecerna:
                    blackFigs.remove(recover_fig)
                else:
                    whiteFigs.remove(recover_fig)
            if type(item) == figurky.Kral:
                item.move2(pole, [move[1], move[2]])
            elif type(item) == figurky.Pesak:
                item.move3(pole, [move[1], move[2]])
            else:
                item.move(pole, [move[1], move[2]])
            pomocna = minimax(pole, hloubka - 1, False, alfa, beta)
            # item.move(pole, backup_coords)
            if type(item) == figurky.Kral:
                item.move2(pole, backup_coords)
            else:
                item.move(pole, backup_coords)
            pole[move[1]][move[2]] = recover_fig
            if recover_fig != '':
                if recover_fig.jecerna:
                    blackFigs.append(recover_fig)
                else:
                    whiteFigs.append(recover_fig)
            hodnota = max(hodnota, pomocna)
            alfa = max(alfa, pomocna)
            if beta <= alfa:
                break
        return hodnota

    else:               # Minimalizující tah
        hodnota = math.inf
        for move in get_moves(pole, ismax):
            item = move[0]
            backup_coords = [item.x, item.y]
            recover_fig = pole[move[1]][move[2]]
            if recover_fig != '':
                if recover_fig.jecerna:
                    blackFigs.remove(recover_fig)
                else:
                    whiteFigs.remove(recover_fig)
            if type(item) == figurky.Pesak or type(item) == figurky.Kral:
                item.move2(pole, [move[1], move[2]])
            elif type(item) == figurky.Pesak:
                item.move3(pole, [move[1], move[2]])
            else:
                item.move(pole, [move[1], move[2]])
            pomocna = minimax(pole, hloubka - 1, True, alfa, beta)
            # item.move(pole, backup_coords)
            if type(item) == figurky.Kral:
                item.move2(pole, backup_coords)
            else:
                item.move(pole, backup_coords)
            pole[move[1]][move[2]] = recover_fig
            if recover_fig != '':
                if recover_fig.jecerna:
                    blackFigs.append(recover_fig)
                else:
                    whiteFigs.append(recover_fig)
            hodnota = min(hodnota, pomocna)
            beta = min(beta, pomocna)
            if beta <= alfa:
                break
        return hodnota


def get_moves(pole, jecerna):
    moznosti = []
    for x in pole:
        for fig in x:
            if fig != '':
                if fig.jecerna == jecerna:
                    # if type(fig) == figurky.Kral:
                    #     for place in fig.kam2(pole):
                    #         moznosti.append([fig, place[0], place[1]])
                    # else:
                    for place in fig.kam(pole):
                        moznosti.append([fig, place[0], place[1]])
                else:
                    # if type(fig) == figurky.Kral:
                    #     for place in fig.kam2(pole):
                    #         moznosti.append([fig, place[0], place[1]])
                    # else:
                    for place in fig.kam(pole):
                        moznosti.append([fig, place[0], place[1]])

    return moznosti


def ohodnoceni(pole):
    soucet = 0
    for x in range(8):
        for y in range(8):
            if pole[x][y] is not '':
                item = pole[x][y]
                if item.jecerna:
                    soucet += (item.hodnota + item.hodnotapozice[x][y])
                else:
                    soucet += ((item.hodnota * (-1)) + item.hodnotapozice[x][y])
    return soucet


def stav(pole):
    # Pat (bílý)    -2
    # Bilý výhra    -1
    # Černy výhra   1
    # Pat (černý)   2
    # Nic           0
    if not pole[figurky.souradnice_b[0]][figurky.souradnice_b[1]].kam(pole):
        if not block(pole, figurky.souradnice_b, whiteFigs, blackFigs):
            if je_v_sachu(pole, figurky.souradnice_b, blackFigs):
                return 1
            else:
                return -2
    if not pole[figurky.souradnice_c[0]][figurky.souradnice_c[1]].kam(pole):
        if not block(pole, figurky.souradnice_c, blackFigs, whiteFigs):
            if je_v_sachu(pole, figurky.souradnice_c, whiteFigs):
                return -1
            else:
                return 2

    return 0
