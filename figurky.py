import pygame
import funkce as fce


# Třídy
class Figurka:
    def __init__(self, jecerna, x, y):
        self.jecerna = jecerna
        self.alive = True
        self.x = x
        self.y = y
        self.this = pygame.image.load("obrazky/NotFound.png")

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
            self.this = pygame.image.load("obrazky/black_king.png")
        else:
            self.this = pygame.image.load("obrazky/white_king.png")
        pole[self.x][self.y] = self
        self.moved = False

    def kam(self, pole):
        sug = []
        x_kolik = 3
        y_kolik = 3
        x_zacatek = self.x-1
        y_zacatek = self.y-1
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
                    if pole[x_zacatek+x][y_zacatek+y] is '' or pole[x_zacatek+x][y_zacatek+y].jecerna is not self.jecerna:
                        sug.append([x_zacatek+x, y_zacatek+y])
        if not self.moved:
            if self.x+3 <= 7 and type(pole[self.x+3][self.y]) == Vez:   # Krátká rošáda na pravou stranu
                if pole[self.x+1][self.y] == '' and pole[self.x+2][self.y] == '':
                    if not fce.je_v_sachu(pole, [self.x, self.y], self.jecerna) and not fce.je_v_sachu(pole, [self.x+1, self.y], self.jecerna) and not fce.je_v_sachu(pole, [self.x+2, self.y], self.jecerna):
                        sug.append([self.x+2, self.y])
            if self.x-4 >= 0 and type(pole[self.x-4][self.y]) == Vez:   # Dlouhá rošáda na levou stranu
                if pole[self.x-1][self.y] == '' and pole[self.x-2][self.y] == '' and pole[self.x-3][self.y] == '':
                    if not fce.je_v_sachu(pole, [self.x, self.y], self.jecerna) and not fce.je_v_sachu(pole, [self.x-1, self.y], self.jecerna) and not fce.je_v_sachu(pole, [self.x-2, self.y], self.jecerna):
                        sug.append([self.x-2, self.y])
        return sug

    def move(self, pole, where):
        if self.x+2 == where[0]:
            vez = pole[self.x+3][self.y]
            pole[self.x][self.y] = ''
            pole[self.x + 3][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            vez.x = self.x-1
            vez.y = self.y
            pole[self.x][self.y] = self
            pole[vez.x][vez.y] = vez
        elif self.x-2 == where[0]:
            vez = pole[self.x-4][self.y]
            pole[self.x][self.y] = ''
            pole[self.x-4][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            vez.x = self.x+1
            vez.y = self.y
            pole[self.x][self.y] = self
            pole[vez.x][vez.y] = vez
        else:
            pole[self.x][self.y] = ''
            self.x = where[0]
            self.y = where[1]
            pole[self.x][self.y] = self


class Kralovna(Figurka):
    def __init__(self, jecerna, x, y, pole):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_queen.png")
        else:
            self.this = pygame.image.load("obrazky/white_queen.png")
        pole[self.x][self.y] = self

    def kam(self, pole):
        sug = []
        x, y = self.x+1, self.y+1
        while x <= 7 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
            y += 1
        x, y = self.x-1, self.y+1
        while x >= 0 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y += 1
        x, y = self.x-1, self.y-1
        while x >= 0 and y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y -= 1
        x, y = self.x+1, self.y-1
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


class Strelec(Figurka):
    def __init__(self, jecerna, x, y, pole):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_bishop.png")
        else:
            self.this = pygame.image.load("obrazky/white_bishop.png")
        pole[self.x][self.y] = self

    def kam(self, pole):
        sug = []
        x, y = self.x+1, self.y+1
        while x <= 7 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
            y += 1
        x, y = self.x-1, self.y+1
        while x >= 0 and y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y += 1
        x, y = self.x-1, self.y-1
        while x >= 0 and y >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
            y -= 1
        x, y = self.x+1, self.y-1
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
    def __init__(self, jecerna, x, y, pole):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_knight.png")
        else:
            self.this = pygame.image.load("obrazky/white_knight.png")
        pole[self.x][self.y] = self

    def kam(self, pole):
        sug = []
        # TODO Tohle oprav (je to prostě zrůdnost ale funguje to xD)
        if self.x+1 <= 7 and self.y-2 >= 0 and (pole[self.x+1][self.y-2] is '' or pole[self.x+1][self.y-2].jecerna is not self.jecerna):
            sug.append([self.x+1, self.y-2])
        if self.x+2 <= 7 and self.y-1 >= 0 and (pole[self.x+2][self.y-1] is '' or pole[self.x+2][self.y-1].jecerna is not self.jecerna):
            sug.append([self.x+2, self.y-1])
        if self.x+2 <= 7 and self.y+1 <= 7 and (pole[self.x+2][self.y+1] is '' or pole[self.x+2][self.y+1].jecerna is not self.jecerna):
            sug.append([self.x+2, self.y+1])
        if self.x+1 <= 7 and self.y+2 <= 7 and (pole[self.x+1][self.y+2] is '' or pole[self.x+1][self.y+2].jecerna is not self.jecerna):
            sug.append([self.x+1, self.y+2])
        if self.x-1 >= 0 and self.y+2 <= 7 and (pole[self.x-1][self.y+2] is '' or pole[self.x-1][self.y+2].jecerna is not self.jecerna):
            sug.append([self.x-1, self.y+2])
        if self.x-2 >= 0 and self.y+1 <= 7 and (pole[self.x-2][self.y+1] is '' or pole[self.x-2][self.y+1].jecerna is not self.jecerna):
            sug.append([self.x-2, self.y+1])
        if self.x-2 >= 0 and self.y-1 >= 0 and (pole[self.x-2][self.y-1] is '' or pole[self.x-2][self.y-1].jecerna is not self.jecerna):
            sug.append([self.x-2, self.y-1])
        if self.x-1 >= 0 and self.y-2 >= 0 and (pole[self.x-1][self.y-2] is '' or pole[self.x-1][self.y-2].jecerna is not self.jecerna):
            sug.append([self.x-1, self.y-2])

        return sug


class Vez(Figurka):
    def __init__(self, jecerna, x, y, pole):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_rook.png")
        else:
            self.this = pygame.image.load("obrazky/white_rook.png")
        pole[self.x][self.y] = self
        self.moved = False

    def kam(self, pole):
        sug = []
        x, y = self.x+1, self.y
        while x <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x += 1
        x = self.x-1
        while x >= 0:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            x -= 1
        x, y = self.x, self.y+1
        while y <= 7:
            if pole[x][y] is '':
                sug.append([x, y])
            else:
                if pole[x][y].jecerna is not self.jecerna:
                    sug.append([x, y])
                break
            y += 1
        y = self.y-1
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
    def __init__(self, jecerna, x, y, pole):
        super().__init__(jecerna, x, y)
        if jecerna:
            self.this = pygame.image.load("obrazky/black_pawn.png")
        else:
            self.this = pygame.image.load("obrazky/white_pawn.png")
        pole[self.x][self.y] = self

    def kam(self, pole):
        sug = []
        if self.jecerna:
            if pole[self.x][self.y+1] is '':
                if self.y is 1 and pole[self.x][self.y+2] is '':
                    sug.append([self.x, self.y+2])
                sug.append([self.x, self.y+1])
            if self.x != 7:
                if pole[self.x+1][self.y+1] is not '' and pole[self.x+1][self.y+1].jecerna is not self.jecerna:
                    sug.append([self.x+1, self.y+1])
            if self.x != 0:
                if pole[self.x-1][self.y+1] is not '' and pole[self.x-1][self.y+1].jecerna is not self.jecerna:
                    sug.append([self.x-1, self.y+1])
        else:
            if pole[self.x][self.y-1] is '':
                if self.y is 6 and pole[self.x][self.y-2] is '':
                    sug.append([self.x, self.y-2])
                sug.append([self.x, self.y-1])
            if self.x != 0:
                if pole[self.x-1][self.y-1] is not '' and pole[self.x-1][self.y-1].jecerna is not self.jecerna:
                    sug.append([self.x-1, self.y-1])
            if self.x != 7:
                if pole[self.x+1][self.y-1] is not '' and pole[self.x+1][self.y-1].jecerna is not self.jecerna:
                    sug.append([self.x+1, self.y-1])
        return sug

    def move(self, pole, where):
        pole[self.x][self.y] = ''
        self.x = where[0]
        self.y = where[1]
        if self.jecerna:
            if self.y == 7:
                ktera = fce.vyber()
                if ktera == 'Kralovna':
                    pole[self.x][self.y] = Kralovna(self.jecerna, self.x, self.y, pole)
                elif ktera == 'Strelec':
                    pole[self.x][self.y] = Strelec(self.jecerna, self.x, self.y, pole)
                elif ktera == 'Kun':
                    pole[self.x][self.y] = Kun(self.jecerna, self.x, self.y, pole)
                elif ktera == 'Vez':
                    pole[self.x][self.y] = Vez(self.jecerna, self.x, self.y, pole)
            else:
                pole[self.x][self.y] = self
        else:
            if self.y == 0:
                ktera = fce.vyber()
                if ktera == 'Kralovna':
                    pole[self.x][self.y] = Kralovna(self.jecerna, self.x, self.y, pole)
                elif ktera == 'Strelec':
                    pole[self.x][self.y] = Strelec(self.jecerna, self.x, self.y, pole)
                elif ktera == 'Kun':
                    pole[self.x][self.y] = Kun(self.jecerna, self.x, self.y, pole)
                elif ktera == 'Vez':
                    pole[self.x][self.y] = Vez(self.jecerna, self.x, self.y, pole)
            else:
                pole[self.x][self.y] = self
