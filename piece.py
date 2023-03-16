import pygame as pg
from const import *

class Piece():
    def __init__(self, screen, name, color, image, row, col):
        self.name = name
        self.color = color
        self.image = image
        self.screen = screen

        self.row = row
        self.col = col

    def draw(self):
        rect = self.image.get_rect()
        rect.left = self.row * SQUARE_SIZE
        rect.top = self.col * SQUARE_SIZE
        self.screen.blit(self.image, rect)


class Pawn(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)

class Knight(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_knight.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_knight.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)



