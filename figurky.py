import pygame
from variables import *
import funkce as fce


souradnice_b = []
souradnice_c = []


# Třídy
class Figurka:
    def __init__(self, jecerna, x, y):
        self.jecerna = jecerna
        self.alive = True
        self.x = x
        self.y = y
        self.this = pygame.image.load("obrazky/NotFound.png")
        self.hodnota = 0
        self.hodnotapozice = []

    def draw(self, window):
        window.blit(self.this, (self.x * 100, self.y * 100))

    def move(self, pole, where):
        pole[self.x][self.y] = ''
        self.x = where[0]
        self.y = where[1]
        pole[self.x][self.y] = self


class Kral(Figurka):
    def __init__(self, jecerna, x, y, pole):
        super().__init__(jecerna, x, y)
        if jecerna:
            global souradnice_c
            souradnice_c = [self.x, self.y]
            self.this = pygame.image.load("obrazky/black_king.png")
            self.hodnotapozice = [
                [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
                [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            ]
        else:
            global souradnice_b
            souradnice_b = [self.x, self.y]
            self.this = pygame.image.load("obrazky/white_king.png")
            self.hodnotapozice = [
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
            ]
        pole[self.x][self.y] = self
        self.moved = False
        self.hodnota = 900

    def kam(self, pole):
        sug = []
        x_kolik = 3
        y_kolik = 3
        x_zacatek = self.x - 1
        y_zacatek = self.y - 1
        if self.x == 0:
            x_kolik = 2
            x_zacatek = self.x
        elif self.x == 7:
            x_kolik = 2
        if self.y == 0:
            y_kolik = 2
            y_zacatek = self.y
        elif self.y == 7:
            y_kolik = 2

        for x in range(x_kolik):
            for y in range(y_kolik):
                if x == self.x and y == self.y:
                    continue
                else:
                    if pole[x_zacatek + x][y_zacatek + y] is '' or pole[x_zacatek + x][
                        y_zacatek + y].jecerna is not self.jecerna:
                        sug.append([x_zacatek + x, y_zacatek + y])
        if self.jecerna:
            enemy_pole = whiteFigs
        else:
            enemy_pole = blackFigs
        # Rošáda
        if not self.moved:
            if self.x + 3 <= 7 and type(pole[self.x + 3][self.y]) == Vez:  # Krátká rošáda na pravou stranu
                if pole[self.x + 1][self.y] == '' and pole[self.x + 2][self.y] == '':
                    if not fce.je_v_sachu(pole, [self.x, self.y], enemy_pole) and not fce.je_v_sachu(pole, [self.x + 1,
                                                                                                            self.y],
                                                                                                     enemy_pole) and not fce.je_v_sachu(
                        pole, [self.x + 2, self.y], enemy_pole):
                        sug.append([self.x + 2, self.y])
            if self.x - 4 >= 0 and type(pole[self.x - 4][self.y]) == Vez:  # Dlouhá rošáda na levou stranu
                if pole[self.x - 1][self.y] == '' and pole[self.x - 2][self.y] == '' and pole[self.x - 3][self.y] == '':
                    if not fce.je_v_sachu(pole, [self.x, self.y], enemy_pole) and not fce.je_v_sachu(pole, [self.x - 1,
                                                                                                            self.y],
                                                                                                     enemy_pole) and not fce.je_v_sachu(
                        pole, [self.x - 2, self.y], enemy_pole):
                        sug.append([self.x - 2, self.y])
        pole[self.x][self.y] = ''
        for i in range(len(sug) - 1, -1, -1):
            if pole[sug[i][0]][sug[i][1]] != '':
                pole[sug[i][0]][sug[i][1]].jecerna = not pole[sug[i][0]][sug[i][1]].jecerna
            if fce.je_v_sachu(pole, sug[i], enemy_pole):
                if pole[sug[i][0]][sug[i][1]] != '':
                    pole[sug[i][0]][sug[i][1]].jecerna = not pole[sug[i][0]][sug[i][1]].jecerna
                del sug[i]
            else:
                if pole[sug[i][0]][sug[i][1]] != '':
                    pole[sug[i][0]][sug[i][1]].jecerna = not pole[sug[i][0]][sug[i][1]].jecerna
        pole[self.x][self.y] = self
        return sug

    def kam2(self, pole):
        sug = []
        x_kolik = 3
        y_kolik = 3
        x_zacatek = self.x - 1
        y_zacatek = self.y - 1
        if self.x == 0:
            x_kolik = 2
            x_zacatek = self.x
        elif self.x == 7:
            x_kolik = 2
        if self.y == 0:
            y_kolik = 2
            y_zacatek = self.y
        elif self.y == 7:
            y_kolik = 2

        for x in range(x_kolik):
            for y in range(y_kolik):
                if x == self.x and y == self.y:
                    continue
                else:
                    if pole[x_zacatek + x][y_zacatek + y] is '' or pole[x_zacatek + x][
                        y_zacatek + y].jecerna is not self.jecerna:
                        sug.append([x_zacatek + x, y_zacatek + y])
        return sug

    def move(self, pole, where):
        if self.x + 2 == where[0]:
            vez = pole[self.x + 3][self.y]
            pole[self.x][self.y] = ''
            pole[self.x + 3][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            vez.x = self.x - 1
            vez.y = self.y
            pole[self.x][self.y] = self
            pole[vez.x][vez.y] = vez
        elif self.x - 2 == where[0]:
            vez = pole[self.x - 4][self.y]
            pole[self.x][self.y] = ''
            pole[self.x - 4][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            vez.x = self.x + 1
            vez.y = self.y
            pole[self.x][self.y] = self
            pole[vez.x][vez.y] = vez
        else:
            pole[self.x][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            pole[self.x][self.y] = self

        if self.jecerna:
            global souradnice_c
            souradnice_c = [self.x, self.y]
        else:
            global souradnice_b
            souradnice_b = [self.x, self.y]

    def move2(self, pole, where):
        pole[self.x][self.y] = ''
        self.x = where[0]
        self.y = where[1]
        pole[self.x][self.y] = self
        if self.jecerna:
            global souradnice_c
            souradnice_c = [self.x, self.y]
        else:
            global souradnice_b
            souradnice_b = [self.x, self.y]


class Kralovna(Figurka):
    def __init__(self, jecerna, x, y, pole, hodnota, je_vygenerovana):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_queen.png")
        else:
            self.this = pygame.image.load("obrazky/white_queen.png")
        pole[self.x][self.y] = self
        self.hodnota = 90
        self.je_vygenerovana = je_vygenerovana
        self.hodnotapozice = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]

    def kam(self, pole):
        sug = []
        x, y = self.x + 1, self.y + 1
        while x <= 7 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
            y += 1
        x, y = self.x - 1, self.y + 1
        while x >= 0 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y += 1
        x, y = self.x - 1, self.y - 1
        while x >= 0 and y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y -= 1
        x, y = self.x + 1, self.y - 1
        while x <= 7 and y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
            y -= 1
        x, y = self.x + 1, self.y
        while x <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
        x = self.x - 1
        while x >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
        x, y = self.x, self.y + 1
        while y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            y += 1
        y = self.y - 1
        while y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            y -= 1
        return sug

    def move(self, pole, where):
        # Klasická dáma (originál)
        if not self.je_vygenerovana:
            pole[self.x][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            pole[self.x][self.y] = self
        # Je vygenerová z pěšce
        else:
            self.je_vygenerovana = True
            pole[self.x][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            if self.jecerna:
                blackFigs.remove(self)
                pole[self.x][self.y] = Pesak(self.jecerna, self.x, self.y, pole, 0)
                blackFigs.append(pole[self.x][self.y])
            else:
                whiteFigs.remove(self)
                pole[self.x][self.y] = Pesak(self.jecerna, self.x, self.y, pole, 0)
                whiteFigs.append(pole[self.x][self.y])
            pole[self.x][self.y] = self


class Strelec(Figurka):
    def __init__(self, jecerna, x, y, pole, hodnota):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_bishop.png")
            self.hodnotapozice = [
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
            ]
        else:
            self.this = pygame.image.load("obrazky/white_bishop.png")
            self.hodnotapozice = [
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
                [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
                [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
                [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
            ]
        pole[self.x][self.y] = self
        self.hodnota = 30

    def kam(self, pole):
        sug = []
        x, y = self.x + 1, self.y + 1
        while x <= 7 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
            y += 1
        x, y = self.x - 1, self.y + 1
        while x >= 0 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y += 1
        x, y = self.x - 1, self.y - 1
        while x >= 0 and y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y -= 1
        x, y = self.x + 1, self.y - 1
        while x <= 7 and y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
            y -= 1
        return sug


class Kun(Figurka):
    def __init__(self, jecerna, x, y, pole, hodnota):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_knight.png")
        else:
            self.this = pygame.image.load("obrazky/white_knight.png")
        pole[self.x][self.y] = self
        self.hodnota = 30
        self.hodnotapozice = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]

    def kam(self, pole):
        sug = []
        # TODO Tohle oprav (je to prostě zrůdnost ale funguje to xD)
        if self.x + 1 <= 7 and self.y - 2 >= 0 and (
                pole[self.x + 1][self.y - 2] is '' or pole[self.x + 1][self.y - 2].jecerna is not self.jecerna):
            sug.append([self.x + 1, self.y - 2])
        if self.x + 2 <= 7 and self.y - 1 >= 0 and (
                pole[self.x + 2][self.y - 1] is '' or pole[self.x + 2][self.y - 1].jecerna is not self.jecerna):
            sug.append([self.x + 2, self.y - 1])
        if self.x + 2 <= 7 and self.y + 1 <= 7 and (
                pole[self.x + 2][self.y + 1] is '' or pole[self.x + 2][self.y + 1].jecerna is not self.jecerna):
            sug.append([self.x + 2, self.y + 1])
        if self.x + 1 <= 7 and self.y + 2 <= 7 and (
                pole[self.x + 1][self.y + 2] is '' or pole[self.x + 1][self.y + 2].jecerna is not self.jecerna):
            sug.append([self.x + 1, self.y + 2])
        if self.x - 1 >= 0 and self.y + 2 <= 7 and (
                pole[self.x - 1][self.y + 2] is '' or pole[self.x - 1][self.y + 2].jecerna is not self.jecerna):
            sug.append([self.x - 1, self.y + 2])
        if self.x - 2 >= 0 and self.y + 1 <= 7 and (
                pole[self.x - 2][self.y + 1] is '' or pole[self.x - 2][self.y + 1].jecerna is not self.jecerna):
            sug.append([self.x - 2, self.y + 1])
        if self.x - 2 >= 0 and self.y - 1 >= 0 and (
                pole[self.x - 2][self.y - 1] is '' or pole[self.x - 2][self.y - 1].jecerna is not self.jecerna):
            sug.append([self.x - 2, self.y - 1])
        if self.x - 1 >= 0 and self.y - 2 >= 0 and (
                pole[self.x - 1][self.y - 2] is '' or pole[self.x - 1][self.y - 2].jecerna is not self.jecerna):
            sug.append([self.x - 1, self.y - 2])

        return sug


class Vez(Figurka):
    def __init__(self, jecerna, x, y, pole, hodnota):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_rook.png")
            self.hodnotapozice = [
                [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ]
        else:
            self.this = pygame.image.load("obrazky/white_rook.png")
            self.hodnotapozice = [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
            ]

        pole[self.x][self.y] = self
        self.moved = False
        self.hodnota = 50

    def kam(self, pole):
        sug = []
        x, y = self.x + 1, self.y
        while x <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
        x = self.x - 1
        while x >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
        x, y = self.x, self.y + 1
        while y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            y += 1
        y = self.y - 1
        while y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            y -= 1
        return sug


class Pesak(Figurka):
    def __init__(self, jecerna, x, y, pole, hodnota):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_pawn.png")
            self.hodnotapozice = [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ]
        else:
            self.this = pygame.image.load("obrazky/white_pawn.png")
            self.hodnotapozice = [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
                [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
                [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            ]
        pole[self.x][self.y] = self
        self.hodnota = 10

    def kam(self, pole):
        sug = []
        if self.jecerna:
            if pole[self.x][self.y + 1] is '':
                if self.y is 1 and pole[self.x][self.y + 2] is '':
                    sug.append([self.x, self.y + 2])
                sug.append([self.x, self.y + 1])
            if self.x != 7:
                if pole[self.x + 1][self.y + 1] is not '' and pole[self.x + 1][self.y + 1].jecerna is not self.jecerna:
                    sug.append([self.x + 1, self.y + 1])
            if self.x != 0:
                if pole[self.x - 1][self.y + 1] is not '' and pole[self.x - 1][self.y + 1].jecerna is not self.jecerna:
                    sug.append([self.x - 1, self.y + 1])
        else:
            if pole[self.x][self.y - 1] is '':
                if self.y is 6 and pole[self.x][self.y - 2] is '':
                    sug.append([self.x, self.y - 2])
                sug.append([self.x, self.y - 1])
            if self.x != 0:
                if pole[self.x - 1][self.y - 1] is not '' and pole[self.x - 1][self.y - 1].jecerna is not self.jecerna:
                    sug.append([self.x - 1, self.y - 1])
            if self.x != 7:
                if pole[self.x + 1][self.y - 1] is not '' and pole[self.x + 1][self.y - 1].jecerna is not self.jecerna:
                    sug.append([self.x + 1, self.y - 1])
        return sug

    def move(self, pole, where):
        pole[self.x][self.y] = ''
        self.x = where[0]
        self.y = where[1]
        if self.jecerna:
            if self.y == 7:
                ktera = fce.vyber()
                if ktera == 'Kralovna':
                    blackFigs.remove(self)
                    pole[self.x][self.y] = Kralovna(self.jecerna, self.x, self.y, pole, 0)
                    blackFigs.append(pole[self.x][self.y])
                elif ktera == 'Strelec':
                    blackFigs.remove(self)
                    pole[self.x][self.y] = Strelec(self.jecerna, self.x, self.y, pole, 0)
                    blackFigs.append(pole[self.x][self.y])
                elif ktera == 'Kun':
                    blackFigs.remove(self)
                    pole[self.x][self.y] = Kun(self.jecerna, self.x, self.y, pole, 0)
                    blackFigs.append(pole[self.x][self.y])
                elif ktera == 'Vez':
                    blackFigs.remove(self)
                    pole[self.x][self.y] = Vez(self.jecerna, self.x, self.y, pole, 0)
                    blackFigs.append(pole[self.x][self.y])
            else:
                pole[self.x][self.y] = self
        else:
            if self.y == 0:
                ktera = fce.vyber()
                if ktera == 'Kralovna':
                    whiteFigs.remove(self)
                    pole[self.x][self.y] = Kralovna(self.jecerna, self.x, self.y, pole, 0)
                    whiteFigs.append(pole[self.x][self.y])
                elif ktera == 'Strelec':
                    whiteFigs.remove(self)
                    pole[self.x][self.y] = Strelec(self.jecerna, self.x, self.y, pole, 0)
                    whiteFigs.append(pole[self.x][self.y])
                elif ktera == 'Kun':
                    whiteFigs.remove(self)
                    pole[self.x][self.y] = Kun(self.jecerna, self.x, self.y, pole, 0)
                    whiteFigs.append(pole[self.x][self.y])
                elif ktera == 'Vez':
                    whiteFigs.remove(self)
                    pole[self.x][self.y] = Vez(self.jecerna, self.x, self.y, pole, 0)
                    whiteFigs.append(pole[self.x][self.y])
            else:
                pole[self.x][self.y] = self

    def move2(self, pole, where):
        pole[self.x][self.y] = ''
        self.x = where[0]
        self.y = where[1]
        pole[self.x][self.y] = self

    def move3(self, pole, where):
        pole[self.x][self.y] = ''
        self.x = where[0]
        self.y = where[1]
        if self.jecerna and self.y == 7:
            blackFigs.remove(self)
            pole[self.x][self.y] = Kralovna(self.jecerna, self.x, self.y, pole, 0, True)
            blackFigs.append(pole[self.x][self.y])
        elif not self.jecerna and self.y == 0:
            whiteFigs.remove(self)
            pole[self.x][self.y] = Kralovna(self.jecerna, self.x, self.y, pole, 0, True)
            whiteFigs.append(pole[self.x][self.y])
        else:
            pole[self.x][self.y] = self
