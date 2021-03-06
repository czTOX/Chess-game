import pygame
import funkce as fce
import scoreboard as sb
import variables as vb
import ai
import chess


# Funkce
def vykresli():
    window = pygame.display.set_mode((sirka, vyska))
    pygame.display.set_caption("Šachy")
    window.blit(background, [0, 0])
    window.blit(title, (130, 40))
    game1.draw(window, 5)
    game2.draw(window, 5)
    scoreboard.draw(window, 5)
    end.draw(window, 5)


def single():
    fce.name_tab(1)
    vb.cons()
    ai.main()


def multi():
    fce.name_tab(0)
    vb.cons()
    chess.main()


def score():
    sb.main()


# Inicializace pygame
pygame.init()

# Konstanty
run = True
sirka = 400
vyska = 560
color = [30, 144, 255]
color2 = [10, 124, 255]
background = pygame.image.load("obrazky/background.jpg")
game1 = fce.Button(color, 125, 150, 150, 50, 'Hra pro 1 hráče')
game2 = fce.Button(color, 125, 250, 150, 50, 'Hra pro 2 hráče')
scoreboard = fce.Button(color, 125, 350, 150, 50, 'Žebříček')
end = fce.Button(color, 125, 450, 150, 50, 'Ukončit hru')
font = pygame.font.SysFont('trebuchetms', 60)
title = font.render("Šachy", 1, (0, 0, 0))


# Základní info pro okno
window = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption("Šachy")


# Hlavní smyčka
while run:
    vykresli()
    pygame.display.update()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        # Quit game
        if event.type == pygame.QUIT:
            run = False

        # Mouse over button
        if event.type == pygame.MOUSEMOTION:
            if game1.over(pos):
                game1.color = color2
            else:
                game1.color = color
            if game2.over(pos):
                game2.color = color2
            else:
                game2.color = color
            if scoreboard.over(pos):
                scoreboard.color = color2
            else:
                scoreboard.color = color
            if end.over(pos):
                end.color = color2
            else:
                end.color = color

        # Button Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game1.over(pos):
                single()
            elif game2.over(pos):
                multi()
            elif scoreboard.over(pos):
                score()
            elif end.over(pos):
                run = False
