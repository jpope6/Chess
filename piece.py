import pygame as pg
from const import *

class Piece():
    def __init__(self, screen, name, color, image, row, col):
        self.name = name
        self.color = color
        self.image = image
        self.screen = screen
        self.move_speed = 1

        self.row = row
        self.col = col
        self.x = row * SQUARE_SIZE
        self.y = col * SQUARE_SIZE

        self.active = False
        self.possible_moves = []

        self.moving = False

    def draw(self, row, col):
        rect = self.image.get_rect()
        rect.left = row
        rect.top = col
        self.screen.blit(self.image, rect)

    def draw_moves(self):
        for move in self.possible_moves:
            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
            pg.draw.circle(surface, (0, 0, 0, 50) , (SQUARE_SIZE / 2, SQUARE_SIZE / 2), 15)
            scaled_move = (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE)
            self.screen.blit(surface, (scaled_move))

class Pawn(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)
            
        self.hasMoved = False
        self.setPossibleMoves()

    
    def setPossibleMoves(self):
        if self.hasMoved:
            self.possible_moves = [(4, 4)]
        if not self.hasMoved:
            self.possible_moves = [(self.row, self.col - 1), (self.row, self.col - 2)]
    

class Knight(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_knight.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_knight.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)

class Rook(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_rook.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_rook.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)

class Bishop(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)

class Queen(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_queen.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_queen.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)

class King(Piece):
    def __init__(self, screen, name, row, col):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_king.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_king.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col)
