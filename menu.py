import pygame
from funkce import name_tab


# Třídy
class button():
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
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def over(self, pos):
        # pos[0] > self.x and pos[0] < self.x + self.width
        if self.x < pos[0] < self.x + self.width:
            # pos[1] > self.y and pos[1] < self.y + self.height
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


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
    name_tab(1)
    import variables
    import ai


def multi():
    name_tab(0)
    import variables
    import chess


def score():
    import scoreboard


# Inicializace pygame
pygame.init()

# Konstanty
run = True
sirka = 400
vyska = 560
color = [30, 144, 255]
color2 = [10, 124, 255]
background = pygame.image.load("obrazky/background.jpg")
game1 = button(color, 125, 150, 150, 50, 'Hra pro 1 hráče')
game2 = button(color, 125, 250, 150, 50, 'Hra pro 2 hráče')
scoreboard = button(color, 125, 350, 150, 50, 'Žebříček')
end = button(color, 125, 450, 150, 50, 'Ukončit hru')
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
