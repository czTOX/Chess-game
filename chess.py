# Knihovny
import pygame
import figurky
import funkce as fce
import math
import ctypes
from variables import *
import scoreboard as sb


def main():
    # Konstanty
    width = 1400
    height = 800
    run = True
    selected = False
    sug = []
    ktera_tahne = True
    item = figurky.Figurka
    sach = False

    pygame.init()
    start_ticks = pygame.time.get_ticks()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Šachy")
    font = pygame.font.SysFont('arial', 25)
    window.fill([212, 241, 249])
    background = pygame.image.load("obrazky/background.jpg")
    window.blit(background, [800, 0])
    pole = [['' for x in range(8)] for y in range(8)]

    kral_c = figurky.Kral(True, 4, 0, pole)
    blackFigs.append(kral_c)
    kral_b = figurky.Kral(False, 4, 7, pole)
    whiteFigs.append(kral_b)
    blackFigs.append(figurky.Kralovna(True, 3, 0, pole, 0, False))
    whiteFigs.append(figurky.Kralovna(False, 3, 7, pole, 0, False))
    blackFigs.append(figurky.Strelec(True, 2, 0, pole, 0)),
    blackFigs.append(figurky.Strelec(True, 5, 0, pole, 0)),
    whiteFigs.append(figurky.Strelec(False, 2, 7, pole, 0)),
    whiteFigs.append(figurky.Strelec(False, 5, 7, pole, 0))
    blackFigs.append(figurky.Kun(True, 1, 0, pole, 0)),
    blackFigs.append(figurky.Kun(True, 6, 0, pole, 0)),
    whiteFigs.append(figurky.Kun(False, 1, 7, pole, 0)),
    whiteFigs.append(figurky.Kun(False, 6, 7, pole, 0))
    blackFigs.append(figurky.Vez(True, 0, 0, pole, 0)),
    blackFigs.append(figurky.Vez(True, 7, 0, pole, 0)),
    whiteFigs.append(figurky.Vez(False, 0, 7, pole, 0)),
    whiteFigs.append(figurky.Vez(False, 7, 7, pole, 0))
    for i in range(8):
        blackFigs.append(figurky.Pesak(True, i, 1, pole, 0))
        whiteFigs.append(figurky.Pesak(False, i, 6, pole, 0))

    fce.vykresli_sachovnici(window, 800)
    fce.vykresli_pole(window, pole)

    image_user = pygame.image.load("obrazky/user.png")
    window.blit(image_user, [1225, 75])
    window.blit(image_user, [1225, 625])
    pygame.display.update()

    dead = []

    # Hlavní smyčka
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = math.floor(x / 100)
                y = math.floor(y / 100)
                if x <= 7:
                    if selected:
                        if [x, y] in sug:
                            backup_coords = [item.x, item.y]
                            recover_fig = ''
                            if pole[x][y] is not '':
                                recover_fig = pole[x][y]
                            if type(item) == figurky.Pesak or type(item) == figurky.Kral:
                                item.move2(pole, [x, y])
                            else:
                                item.move(pole, [x, y])
                            if ktera_tahne:
                                if recover_fig is not '':
                                    blackFigs.remove(recover_fig)
                                if fce.je_v_sachu(pole, [kral_b.x, kral_b.y], blackFigs):
                                    print("bily je v sachu")
                                    ctypes.windll.user32.MessageBoxW(0, 'Takto táhnout nemůžeš. Král je v šachu.',
                                                                     'Nedovolený tah', 1)
                                    item.move(pole, backup_coords)
                                    pole[x][y] = recover_fig
                                    if recover_fig is not '':
                                        blackFigs.append(recover_fig)
                                else:
                                    if recover_fig is not '':
                                        blackFigs.append(recover_fig)
                                    item.move(pole, backup_coords)
                                    pole[x][y] = recover_fig
                                    if pole[x][y] is not '':
                                        blackFigs.remove(pole[x][y])
                                        dead.append(pole[x][y])
                                        fce.vypis_mrtvych(window, dead)
                                    item.move(pole, [x, y])
                                    selected = False
                                    ktera_tahne = not ktera_tahne
                                    fce.refresh(window, pole)
                                    if fce.je_mat(pole, [kral_c.x, kral_c.y], blackFigs, whiteFigs):
                                        fce.zapis_skore(seconds)
                                        ctypes.windll.user32.MessageBoxW(0, 'Bílý vyhrál! :)', 'Konec hry!', 1)
                                        run = False
                                        break
                                    elif fce.pat(pole, [kral_c.x, kral_c.y], blackFigs, whiteFigs):
                                        ctypes.windll.user32.MessageBoxW(0, 'Pat! :)', 'Konec hry!', 1)
                                        run = False
                                        break
                            else:
                                if recover_fig is not '':
                                    whiteFigs.remove(recover_fig)
                                if fce.je_v_sachu(pole, [kral_c.x, kral_c.y], whiteFigs):
                                    print("cerny je v sachu")
                                    ctypes.windll.user32.MessageBoxW(0, 'Takto táhnout nemůžeš. Král je v šachu.',
                                                                     'Nedovolený tah', 1)
                                    item.move(pole, backup_coords)
                                    pole[x][y] = recover_fig
                                    if recover_fig is not '':
                                        whiteFigs.append(recover_fig)
                                else:
                                    item.move(pole, backup_coords)
                                    pole[x][y] = recover_fig
                                    if recover_fig is not '':
                                        whiteFigs.append(recover_fig)
                                    if pole[x][y] is not '':
                                        whiteFigs.remove(pole[x][y])
                                        dead.append(pole[x][y])
                                        fce.vypis_mrtvych(window, dead)
                                    item.move(pole, [x, y])
                                    selected = False
                                    ktera_tahne = not ktera_tahne
                                    fce.refresh(window, pole)
                                    if fce.je_mat(pole, [kral_b.x, kral_b.y], whiteFigs, blackFigs):
                                        fce.zapis_skore(seconds)
                                        ctypes.windll.user32.MessageBoxW(0, 'Černý vyhrál! :)', 'Konec hry!', 1)
                                        run = False
                                        break
                                    elif fce.pat(pole, [kral_b.x, kral_b.y], whiteFigs, blackFigs):
                                        ctypes.windll.user32.MessageBoxW(0, 'Pat! :)', 'Konec hry!', 1)
                                        run = False
                                        break
                        elif pole[x][y] is '' or pole[x][y] is item or pole[x][y].jecerna is ktera_tahne:
                            selected = False
                            fce.refresh(window, pole)
                        elif pole[x][y].jecerna is item.jecerna:
                            item = pole[x][y]
                            sug = item.kam(pole)
                            fce.refresh(window, pole)
                            fce.vyresli_moznosti(window, sug)
                            pygame.display.update()
                        else:
                            fce.refresh(window, pole)
                            selected = False
                    else:
                        if pole[x][y] is not '':
                            if pole[x][y].jecerna is not ktera_tahne:
                                selected = True
                                item = pole[x][y]
                                sug = item.kam(pole)
                                fce.vyresli_moznosti(window, sug)
                                pygame.display.update()
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        text = font.render(("%02d:%02d" % (math.floor(seconds) / 60, math.floor(seconds) % 60)), True, [0, 0, 0])
        pygame.draw.rect(window, [255, 255, 255], (1296, 355, 70, 30))
        window.blit(text, [1300, 355])
        pygame.display.update()
