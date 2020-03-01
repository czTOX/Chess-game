import tkinter as tk
import math
import ctypes
import os
import pygame
import funkce as fce


# file = open('zebricek.txt', 'r')
# if os.stat("zebricek.txt").st_size != 0:
#     scoreboard = tk.Tk()
#     scoreboard.geometry('400x600')
#     scoreboard.title('Scoreboard')
#     for line in file:
#         s = line.split(';')
#         time = ("%02d:%02d" % (math.floor(float(s[2]))/60, math.floor(float(s[2])) % 60))
#         text = s[0] + " porazil/a " + s[1] + " v čase: " + time
#         label = tk.Label(scoreboard, text=text).pack()
#     scoreboard.mainloop()
# else:
#     ctypes.windll.user32.MessageBoxW(0, 'Zatím není ve výsledcích ani jedna hra :(', 'File is empty', 1)


def main():
    # Funkce
    def vykresli():
        win = pygame.display.set_mode((sirka, vyska))
        pygame.display.set_caption("Žebříček")
        win.blit(background, [0, 0])
        win.blit(title, (67, 40))
        zpet.draw(win, 5)

    # Inicializace pygame
    pygame.init()

    # Konstanty
    run = True
    sirka = 400
    vyska = 600
    color = [30, 144, 255]
    color2 = [10, 124, 255]
    background = pygame.image.load("obrazky/background.jpg")
    zpet = fce.Button(color, 125, 450, 150, 50, 'Zpět')
    font = pygame.font.SysFont('trebuchetms', 35, bold=True)
    font.set_underline(True)
    title = font.render("Nejrychlejší hry", 1, (0, 0, 0))
    font = pygame.font.SysFont('trebuchetms', 20)

    # Základní info pro okno
    win = pygame.display.set_mode((sirka, vyska))
    pygame.display.set_caption("Žebříček")

    file = open('zebricek.txt', 'r')
    if os.stat("zebricek.txt").st_size != 0:
        vykresli()
        a = []
        y = 0
        for line in file:
            s = line.split(';')
            s[2] = s[2].rstrip('\n')
            a.append(s)
        a = sorted(a, key=lambda x: x[1])
        for zapis in a:
            time = ("%02d:%02d" % (math.floor(float(zapis[1])) / 60, math.floor(float(zapis[1])) % 60))
            text = zapis[0] + " porazil/a " + zapis[2] + " v čase: " + time
            label = font.render(text, 1, (0, 0, 0))
            win.blit(label, [63, 125 + y])
            y += 25
            if y >= 250:
                break
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEMOTION:
                    if zpet.over(pos):
                        zpet.color = color2
                    else:
                        zpet.color = color

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if zpet.over(pos):
                        run = False
    else:
        ctypes.windll.user32.MessageBoxW(0, 'Zatím není ve výsledcích ani jedna hra :(', 'File is empty', 1)
