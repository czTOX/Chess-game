# Knihovny
import pygame
import figurky
import funkce as fce
import math
import ctypes

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
kral_b = figurky.Kral(False, 4, 7, pole)
kralovna = figurky.Kralovna(True, 3, 0, pole), \
           figurky.Kralovna(False, 3, 7, pole)
strelec = figurky.Strelec(True, 2, 0, pole), \
          figurky.Strelec(True, 5, 0, pole), \
          figurky.Strelec(False, 2, 7, pole),\
          figurky.Strelec(False, 5, 7, pole)
kun = figurky.Kun(True, 1, 0, pole), \
         figurky.Kun(True, 6, 0, pole), \
         figurky.Kun(False, 1, 7, pole), \
         figurky.Kun(False, 6, 7, pole)
vez = figurky.Vez(True, 0, 0, pole), \
      figurky.Vez(True, 7, 0, pole), \
      figurky.Vez(False, 0, 7, pole), \
      figurky.Vez(False, 7, 7, pole)
for i in range(8):
    figurky.Pesak(True, i, 1, pole)
    figurky.Pesak(False, i, 6, pole)

fce.vykresli_sachovnici(window, 800)
fce.vykresli_pole(window, pole)

image_user = pygame.image.load("obrazky/user.png")
image_ai = pygame.image.load("obrazky/ai.png")
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
            x = math.floor(x/100)
            y = math.floor(y/100)
            if x <= 7:
                if selected:
                    if [x, y] in sug:
                        # TODO přidat rámeček kolem hráče, ať jde vidět kdo je na tahu
                        backup_coords = [item.x, item.y]
                        recover_fig = ''
                        if pole[x][y] is not '':
                            recover_fig = pole[x][y]
                        item.move(pole, [x, y])
                        if ktera_tahne:
                            if fce.je_v_sachu(pole, [kral_b.x, kral_b.y], False):
                                ctypes.windll.user32.MessageBoxW(0, 'Takto táhnout nemůžeš. Král je v šachu.', 'Nedovolený tah', 1)
                                item.move(pole, backup_coords)
                                pole[x][y] = recover_fig
                            else:
                                item.move(pole, backup_coords)
                                pole[x][y] = recover_fig
                                if pole[x][y] is not '':
                                    dead.append(pole[x][y])
                                    fce.vypis_mrtvych(window, dead)
                                item.move(pole, [x, y])
                                selected = False
                                ktera_tahne = not ktera_tahne
                                fce.refresh(window, pole)
                        else:
                            if fce.je_v_sachu(pole, [kral_c.x, kral_c.y], True):
                                ctypes.windll.user32.MessageBoxW(0, 'Takto táhnout nemůžeš. Král je v šachu.', 'Nedovolený tah', 1)
                                item.move(pole, backup_coords)
                                pole[x][y] = recover_fig
                            else:
                                item.move(pole, backup_coords)
                                pole[x][y] = recover_fig
                                if pole[x][y] is not '':
                                    dead.append(pole[x][y])
                                    fce.vypis_mrtvych(window, dead)
                                item.move(pole, [x, y])
                                selected = False
                                ktera_tahne = not ktera_tahne
                                fce.refresh(window, pole)
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
    text = font.render(("%02d:%02d" % (math.floor(seconds)/60, math.floor(seconds) % 60)), True, [0, 0, 0])
    pygame.draw.rect(window, [255, 255, 255], (1300, 355, 60, 30))
    window.blit(text, [1300, 355])
    pygame.display.update()
