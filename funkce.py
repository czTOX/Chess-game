# Knihovny
import pygame
import tkinter as tk
import figurky
from variables import *
import random


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
                friend.move(pole, backup_coords)
                pole[place[0]][place[1]] = recover_fig
                if recover_fig is not '':
                    enemy_figs.append(recover_fig)
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
            if block(pole, souradnice, friendly_figs, enemy_figs):
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
            print(names)
            names.append(textbox1.get())
        else:
            names.append('Player1')
        names.append('AI')
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
        okno.title('Zadej jméno hráče')

        label1 = tk.Label(okno, text='Jméno:')
        label1.pack()
        textbox1 = tk.Entry(okno)
        textbox1.focus_set()
        textbox1.pack()
        button = tk.Button(okno, text='Hrát!', command=play2)
        button.pack()

    okno.mainloop()


# ------------------- AI stuff ------------------- *
def minimax(pole, hloubka, ismax):
    # Pokud už dosáhl určité hloubky
    if hloubka == 0:
        # Parametr ismax předastavuje atribut jecerna
        if ismax:
            hodnota = -1
            best_move = []
            for move in get_moves(pole, ismax):
                if pole[move[1]][move[2]] == '':
                    if hodnota < 0:
                        hodnota = 0
                        best_move = move
                elif pole[move[1]][move[2]].hodnota > hodnota:
                    hodnota = pole[move[1]][move[2]].hodnota
                    best_move = move
            return hodnota, best_move

    if ismax:
        hodnota = -1
        best_move = []
        for move in get_moves(pole, False):
            backup_coords = [move[0].x, move[0].y]
            recover_fig = ''
            if pole[move[1]][move[2]] is not '':
                recover_fig = pole[move[1]][move[2]]
            move[0].move(pole, [move[1], move[2]])
            hodnota_vetve = minimax(pole, hloubka-1, False)
            if hodnota < hodnota_vetve:
                hodnota = hodnota_vetve
                best_move = move
            # Move back
            move[0].move(pole, backup_coords)
            pole[move[1]][move[2]] = recover_fig
        return hodnota, best_move
    else:
        hodnota = 9999
        for move in get_moves(pole, True):
            backup_coords = [move[0].x, move[0].y]
            recover_fig = ''
            if pole[move[1]][move[2]] is not '':
                recover_fig = pole[move[1]][move[2]]
            move[0].move(pole, [move[1], move[2]])
            hodnota_vetve = minimax(pole, hloubka-1, False)
            if hodnota > hodnota_vetve:
                hodnota = hodnota_vetve
            # Move back
            move[0].move(pole, backup_coords)
            pole[move[1]][move[2]] = recover_fig
        return hodnota


def get_moves(pole, jecerna):
    moznosti = []
    for x in pole:
        for fig in x:
            if fig != '':
                if fig.jecerna == jecerna:
                    for place in fig.kam(pole):
                        moznosti.append([fig, place[0], place[1]])
                else:
                    for place in fig.kam(pole):
                        moznosti.append([fig, place[0], place[1]])
    return moznosti


def idk(pole, maximize, depth):
    if depth == 0:
        value = []
        moves = get_moves(pole)
        for i in moves:
            hodnota = 0
            if pole[i[1]][i[2]] != '':
                hodnota = pole[i[1]][i[2]].hodnota
            if hodnota > value:
                value.append(value, i)
        return value       # Vrátí nejlepší větev
    else:
        maximum = 0
        moves = get_moves(pole)
        if maximize:
            for each in moves:
                # Předělat pole aby se nezadávalo pořád stejné
                new = each[0].move(pole, [each[1], each[2]])
                value = idk(new, False, depth-1)
                if value > maximum:
                    maximum = value

                #
        else:
            for each in moves:
                # Předělat pole aby se nezadávalo pořád stejné
                new = each[0].move(pole, [each[1], each[2]])
                value = idk(new, True, depth-1)
                if value > maximum:
                    maximum = value
    return maximum



