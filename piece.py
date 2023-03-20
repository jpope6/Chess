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

    def draw_moves(self):
        if self.captured: return

        for move in self.possible_moves:
            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
            pg.draw.circle(surface, (57, 255, 20, 50) , (SQUARE_SIZE / 2, SQUARE_SIZE / 2), 15)
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
                if self.col == 0: # If you are on the last square of the board
                    pass
                # If there is no piece in front of the pawn
                elif not self.board_map[(self.row, self.col - 1)].piece:
                    self.possible_moves = [(self.row, self.col - 1)]
            else:
                if self.col == 7: # If you are on the last square of the board
                    pass
                elif not self.board_map[(self.row, self.col + 1)].piece:
                    self.possible_moves = [(self.row, self.col + 1)]
            
        # Moves if pawn has not moved yet
        #
        # The max squares that a pawn can move is 2, so check up to 2 squares
        # in front of the pawn and if there is no piece. If there is no piece
        # then I know I can add the square to the possible moves
        if not self.hasMoved:
            index = 1
            if self.color == 'white':
                while index <= 2 and not self.board_map[(self.row, self.col - index)].piece:
                    self.possible_moves.append((self.row, self.col - index))
                    index += 1
            else:
                while index <= 2 and not self.board_map[(self.row, self.col + index)].piece:
                    self.possible_moves.append((self.row, self.col + index))
                    index += 1
                
          
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
        else:
            try: 
                temp = self.board_map[(self.row - 1, self.col + 1)].piece

                if temp and temp.color != self.color:
                    self.possible_moves.append((self.row - 1, self.col + 1))
            except:
                pass

            try: 
                temp = self.board_map[(self.row + 1, self.col + 1)].piece

                if temp and temp.color != self.color:
                    self.possible_moves.append((self.row + 1, self.col + 1))
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

        self.setPossibleMoves()

    def setPossibleMoves(self):
        
        self.possible_moves = []

        # Check (2, 1) and (1, 2) away from the current square  
        # If there is no piece on the checked square or the 
        #   piece is a different color, add it to possible moves

        try:
            temp = self.board_map[(self.row + 2, self.col + 1)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row + 2, self.col + 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 2, self.col + 1)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row - 2, self.col + 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 2, self.col - 1)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row - 2, self.col - 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row + 2, self.col - 1)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row + 2, self.col - 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row + 1, self.col + 2)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row + 1, self.col + 2))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 1, self.col + 2)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row - 1, self.col + 2))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 1, self.col - 2)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row - 1, self.col - 2))
        except:
            pass

        try:
            temp = self.board_map[(self.row + 1, self.col - 2)].piece

            if not temp or temp.color != self.color:
                self.possible_moves.append((self.row + 1, self.col - 2))
        except:
            pass



class Rook(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_rook.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_rook.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

        self.setPossibleMoves()

    def setPossibleMoves(self):
            
        self.possible_moves = []

        up = down = left = right = False

        # Check every row/col on the rooks current square
        # If there is no piece on a square in that direction, add to the possible moves
        # If there is a piece but it is the opposite color, add to possible moves
        #   but stop the movement in that direction
        # If there is a piece of the same color, stop the movement in that direction

        for i in range(0, 8):

            if not up and self.row != self.row + i:
                try:
                    temp = self.board_map[(self.row + i, self.col)].piece

                    if not temp:
                        self.possible_moves.append((self.row + i, self.col))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row + i, self.col))
                        up = True
                    else:
                        up = True
                except:
                    pass

            if not down and self.row != self.row - i:
                try:
                    temp = self.board_map[(self.row - i, self.col)].piece

                    if not temp:
                        self.possible_moves.append((self.row - i, self.col))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row - i, self.col))
                        down = True
                    else:
                        down = True
                except:
                    pass

            if not right and self.col != self.col + i:
                try:
                    temp = self.board_map[(self.row, self.col + i)].piece

                    if not temp:
                        self.possible_moves.append((self.row, self.col + i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row, self.col + i))
                        right = True
                    else:
                        right = True
                except:
                    pass
            
            if not left and self.col != self.col - i:
                try:
                    temp = self.board_map[(self.row, self.col - i)].piece

                    if not temp:
                        self.possible_moves.append((self.row, self.col - i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row, self.col - i))
                        left = True
                    else:
                        left = True
                except:
                    pass


class Bishop(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_bishop.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

        self.setPossibleMoves()

    def setPossibleMoves(self):    

        self.possible_moves = []

        up_left = down_left = up_right = down_right = False

        # Check every diagonal on the bishops current square
        # If there is no piece on a square in that direction, add to the possible moves
        # If there is a piece but it is the opposite color, add to possible moves
        #   but stop the movement in that direction
        # If there is a piece of the same color, stop the movement in that direction

        for i in range(0, 8):

            if not down_right and self.row != self.row + i and self.col != self.col + i:
                try:
                    temp = self.board_map[(self.row + i, self.col + i)].piece

                    if not temp:
                        self.possible_moves.append((self.row + i, self.col + i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row + i, self.col + i))
                        down_right = True
                    else:
                        down_right = True
                except:
                    pass

            if not down_left and self.row != self.row + i and self.col != self.col - i:
                try:
                    temp = self.board_map[(self.row + i, self.col - i)].piece

                    if not temp:
                        self.possible_moves.append((self.row + i, self.col - i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row + i, self.col - i))
                        down_left = True
                    else:
                        down_left = True
                except:
                    pass

            if not up_right and self.row != self.row - i and self.col != self.col + i:
                try:
                    temp = self.board_map[(self.row - i, self.col + i)].piece

                    if not temp:
                        self.possible_moves.append((self.row - i, self.col + i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row - i, self.col + i))
                        up_right = True
                    else:
                        up_right = True
                except:
                    pass
            
            if not up_left and self.row != self.row - i and self.col != self.col - i:
                try:
                    temp = self.board_map[(self.row - i, self.col - i)].piece

                    if not temp:
                        self.possible_moves.append((self.row - i, self.col - i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row - i, self.col - i))
                        up_left = True
                    else:
                        up_left = True
                except:
                    pass

class Queen(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_queen.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_queen.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

    def setPossibleMoves(self):
        
        self.possible_moves = []

        up = down = left = right = up_left = up_right = down_left = down_right = False

        # Basically just combine Bishop and Rook possible moves 

        for i in range(0, 8):

            if not up and self.row != self.row + i:
                try:
                    temp = self.board_map[(self.row + i, self.col)].piece

                    if not temp:
                        self.possible_moves.append((self.row + i, self.col))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row + i, self.col))
                        up = True
                    else:
                        up = True
                except:
                    pass

            if not down and self.row != self.row - i:
                try:
                    temp = self.board_map[(self.row - i, self.col)].piece

                    if not temp:
                        self.possible_moves.append((self.row - i, self.col))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row - i, self.col))
                        down = True
                    else:
                        down = True
                except:
                    pass

            if not right and self.col != self.col + i:
                try:
                    temp = self.board_map[(self.row, self.col + i)].piece

                    if not temp:
                        self.possible_moves.append((self.row, self.col + i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row, self.col + i))
                        right = True
                    else:
                        right = True
                except:
                    pass
            
            if not left and self.col != self.col - i:
                try:
                    temp = self.board_map[(self.row, self.col - i)].piece

                    if not temp:
                        self.possible_moves.append((self.row, self.col - i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row, self.col - i))
                        left = True
                    else:
                        left = True
                except:
                    pass

            if not down_right and self.row != self.row + i and self.col != self.col + i:
                try:
                    temp = self.board_map[(self.row + i, self.col + i)].piece

                    if not temp:
                        self.possible_moves.append((self.row + i, self.col + i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row + i, self.col + i))
                        down_right = True
                    else:
                        down_right = True
                except:
                    pass

            if not down_left and self.row != self.row + i and self.col != self.col - i:
                try:
                    temp = self.board_map[(self.row + i, self.col - i)].piece

                    if not temp:
                        self.possible_moves.append((self.row + i, self.col - i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row + i, self.col - i))
                        down_left = True
                    else:
                        down_left = True
                except:
                    pass

            if not up_right and self.row != self.row - i and self.col != self.col + i:
                try:
                    temp = self.board_map[(self.row - i, self.col + i)].piece

                    if not temp:
                        self.possible_moves.append((self.row - i, self.col + i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row - i, self.col + i))
                        up_right = True
                    else:
                        up_right = True
                except:
                    pass
            
            if not up_left and self.row != self.row - i and self.col != self.col - i:
                try:
                    temp = self.board_map[(self.row - i, self.col - i)].piece

                    if not temp:
                        self.possible_moves.append((self.row - i, self.col - i))
                    elif temp.color != self.color:
                        self.possible_moves.append((self.row - i, self.col - i))
                        up_left = True
                    else:
                        up_left = True
                except:
                    pass


class King(Piece):
    def __init__(self, screen, name, row, col, board_map):
        if name[0] == 'W':
            color = "white"
            image = pg.transform.scale(pg.image.load("./assets/images/white_king.png"), (SQUARE_SIZE, SQUARE_SIZE))
        else:
            color = "black"
            image = pg.transform.scale(pg.image.load("./assets/images/black_king.png"), (SQUARE_SIZE, SQUARE_SIZE))

        super().__init__(screen, name, color, image, row, col, board_map)

        self.setPossibleMoves()

    def setPossibleMoves(self):
        self.possible_moves = []

        # King can only move one square in any direction

        try:
            temp = self.board_map[(self.row + 1, self.col)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row + 1, self.col))
        except:
            pass

        try:
            temp = self.board_map[(self.row + 1, self.col + 1)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row + 1, self.col + 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row, self.col + 1)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row, self.col + 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 1, self.col + 1)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row - 1, self.col + 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 1, self.col)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row - 1, self.col))
        except:
            pass

        try:
            temp = self.board_map[(self.row - 1, self.col - 1)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row - 1, self.col - 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row, self.col - 1)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row, self.col - 1))
        except:
            pass

        try:
            temp = self.board_map[(self.row + 1, self.col - 1)].piece

            if not temp or self.color != temp.color:
                self.possible_moves.append((self.row + 1, self.col - 1))
        except:
            pass
