import pygame as pg
from const import *

class Piece():
    def __init__(self, screen, name, color, image, row, col, board_map):
        self.name = name
        self.color = color
        self.image = image
        self.screen = screen
        self.board_map = board_map

        self.row = row
        self.col = col
        self.x = row * SQUARE_SIZE
        self.y = col * SQUARE_SIZE

        self.active = False
        self.hasMoved = False
        self.possible_moves = []

        self.moving = False

        self.captured = False

    def draw(self, row, col):
        if self.captured: return

        rect = self.image.get_rect()
        rect.left = row
        rect.top = col
        self.screen.blit(self.image, rect)

    def setPossibleMoves(self):
        pass

 
    def draw_moves(self):
        if self.captured: return

        for move in self.possible_moves:
            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
            pg.draw.circle(surface, (255, 0, 0, 50) , (SQUARE_SIZE / 2, SQUARE_SIZE / 2), 15)
            scaled_move = (move[0] * SQUARE_SIZE, move[1] * SQUARE_SIZE)
            self.screen.blit(surface, (scaled_move))


class Pawn(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_pawn.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)
            
        self.setPossibleMoves()

    
    def setPossibleMoves(self):
        # Reset any previous moves 
        self.possible_moves = []

        # Moves if pawn has already moved 
        if self.hasMoved:
            if self.color == "white":
                self.possible_moves = [(self.row, self.col - 1)]
            else:
                self.possible_moves = [(self.row, self.col + 1)]
            
        # Moves if pawn has not moved yet
        if not self.hasMoved:
            if self.color == 'white':
                self.possible_moves = [(self.row, self.col - 1), (self.row, self.col - 2)]
            else:
                self.possible_moves = [(self.row, self.col + 1), (self.row, self.col + 2)]
                
          
        # Moves if there is piece of opposite color on diagonal square 
        if self.color == "white":
            try: 
                temp = self.board_map[(self.row - 1, self.col - 1)].piece

                if temp and temp.color != self.color:
                    self.possible_moves.append((self.row - 1, self.col - 1))
            except:
                pass

            try: 
                temp = self.board_map[(self.row + 1, self.col - 1)].piece

                if temp and temp.color != self.color:
                    self.possible_moves.append((self.row + 1, self.col - 1))
            except:
                pass




class Knight(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_knight.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_knight.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

class Rook(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_rook.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_rook.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

class Bishop(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

class Queen(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_queen.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_queen.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

class King(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_king.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_king.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)
