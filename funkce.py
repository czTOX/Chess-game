# Knihovny
import pygame
import tkinter as tk
import figurky
from variables import *


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


def zapis_skore(jmeno, time):
    zebricek = open("zebricek.txt", "a+")
    zebricek.write(jmeno + ";" + str(time))
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
            # Switchnout pole enemy_figs, a pokud to narazí na krále to ho to přeskočí
            sug = []
            x_kolik = 3
            y_kolik = 3
            x_zacatek = fig.x - 1
            y_zacatek = fig.y - 1
            if fig.x == 0:
                x_kolik = 2
                x_zacatek = fig.x
            elif fig.x == 7:
                x_kolik = 2
            if fig.y == 0:
                y_kolik = 2
                y_zacatek = fig.y
            elif fig.y == 7:
                y_kolik = 2

            for x in range(x_kolik):
                for y in range(y_kolik):
                    if x == fig.x and y == fig.y:
                        continue
                    else:
                        if pole[x_zacatek + x][y_zacatek + y] is '' or pole[x_zacatek + x][y_zacatek + y].jecerna is not fig.jecerna:
                            sug.append([x_zacatek + x, y_zacatek + y])
            if souradnice in sug:
                return True
        elif souradnice in fig.kam(pole):
            return True
    return False


def je_mat(pole, souradnice, enemy_figs):
    # Může se král movnou někam, kde by šach neměl
    pass
