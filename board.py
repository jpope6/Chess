import pygame as pg
import const
from piece import *

# Testing a github thing

class Board():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.board_map = {}
        self.board = self.draw_board_array()
        self.active_piece = None
        self.attacking_piece = None
        self.path_to_king = None

        self.turn = "white"

        self.white_pieces = []
        self.white_moves = []
        self.black_pieces = []
        self.black_moves = []

        self.setMovesForAllPieces()

    def draw_board_array(self):
        board = [["" for j in range(8)] for i in range(8)]

        # Add a map of BoardSquare for easy access to each square
        for i in range(8):
            for j in range(8):
                self.board_map[(i, j)] = BoardSquare(i, j)

        # pawns
        for i in range(8):
            self.board_map[(i, 6)].piece = Pawn(self.screen, "WP", i, 6, self.board_map)
            self.board_map[(i, 1)].piece = Pawn(self.screen, "BP", i, 1, self.board_map)
            

        # Place down the horsies
        self.board_map[(1, 0)].piece = Knight(self.screen, "BH", 1, 0, self.board_map)
        self.board_map[(6, 0)].piece = Knight(self.screen, "BH", 6, 0, self.board_map)
        self.board_map[(1, 7)].piece = Knight(self.screen, "WH", 1, 7, self.board_map)
        self.board_map[(6, 7)].piece = Knight(self.screen, "WH", 6, 7, self.board_map)

        # THE ROOOOOOOOOOOOOOOOOOK
        self.board_map[(0, 0)].piece = Rook(self.screen, "BR", 0, 0, self.board_map)
        self.board_map[(7, 0)].piece = Rook(self.screen, "BR", 7, 0, self.board_map)
        self.board_map[(0, 7)].piece = Rook(self.screen, "WR", 0, 7, self.board_map)
        self.board_map[(7, 7)].piece = Rook(self.screen, "WR", 7, 7, self.board_map)

        #Bishop Boys
        self.board_map[(2, 0)].piece = Bishop(self.screen, "BB", 2, 0, self.board_map)
        self.board_map[(5, 0)].piece = Bishop(self.screen, "BB", 5, 0, self.board_map)
        self.board_map[(2, 7)].piece = Bishop(self.screen, "WB", 2, 7, self.board_map)
        self.board_map[(5, 7)].piece = Bishop(self.screen, "WB", 5, 7, self.board_map)

        # Oh no, my queen
        self.board_map[(3, 0)].piece = Queen(self.screen, "BQ", 3, 0, self.board_map)
        self.board_map[(3, 7)].piece = Queen(self.screen, "WQ", 3, 7, self.board_map)

        # King ****
        self.black_king = King(self.screen, "BK", 4, 0, self.board_map)
        self.white_king = King(self.screen, "WK", 4, 7, self.board_map)
        self.board_map[(4, 0)].piece = self.black_king
        self.board_map[(4, 7)].piece = self.white_king


        print(board)

        return board


    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = const.LIGHT_COLOR
                else:
                    color = const.DARK_COLOR

                pg.draw.rect(self.screen, color, [
                    j * const.SQUARE_SIZE,
                    i * const.SQUARE_SIZE, 
                    const.SQUARE_SIZE,
                    const.SQUARE_SIZE
                    ])

    # If there is a piece on the square, draw it
    def draw_pieces(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.board_map[(i, j)].piece and not self.board_map[(i, j)].piece.moving:
                    self.board_map[(i, j)].piece.draw(i * SQUARE_SIZE, j * SQUARE_SIZE)

        if self.active_piece and self.active_piece.active and self.turn == self.active_piece.color:
            self.active_piece.draw_moves()

    def move(self, row, col):
        if not self.active_piece: return
        if (row, col) not in self.active_piece.possible_moves: return
        if self.turn != self.active_piece.color: return
        
        # The active pieces current square will be empty since it is moving
        self.board_map[(self.active_piece.row, self.active_piece.col)].piece = None

        # If the piece is capturing another piece
        if self.board_map[(row, col)].piece:
            self.board_map[(row, col)].piece.captured = True

        self.board_map[(row, col)].piece = self.active_piece
        self.active_piece.row = row
        self.active_piece.col = col
        self.active_piece.active = False
        self.active_piece.hasMoved = True

        self.setMovesForAllPieces()
        self.checkForCheck()
        
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def checkForCheck(self):
        self.path_to_king = []

        if self.turn == "white":
            for piece in self.white_pieces:
                for move in piece.possible_moves:
                    if move == (self.black_king.row, self.black_king.col):
                        print("check")
                        self.attacking_piece = piece
                        self.path_to_king = self.getAttackingPiecePathToKing()
                        if self.checkForCheckmate():
                            print("checkmate")

                if self.attacking_piece:
                    break

        if self.turn == "black":
            for piece in self.black_pieces:
                for move in piece.possible_moves:
                    if move == (self.white_king.row, self.white_king.col):
                        print("check")
                        self.attacking_piece = piece
                        self.path_to_king = self.getAttackingPiecePathToKing()
                        if self.checkForCheckmate():
                            print("checkmate")

                if self.attacking_piece:
                    break

    
    def checkForCheckmate(self):
        checkmate = True

        if self.turn == "white":
            # Check if there is a move in king moves that will get it out of check
            for move in self.black_king.possible_moves:
                if move not in self.white_moves:
                    checkmate = False

            # Check if there is a piece that can block the path of the attacking_piece
            if self.path_to_king:
                for piece in self.black_pieces:
                    if piece.name[1] != 'K':
                        for move in piece.possible_moves:
                            if move in self.path_to_king:
                                checkmate = False
                            else:
                                piece.possible_moves.remove(move)

        if self.turn == "black":
            # Check if there is a move in king moves that will get it out of check
            for move in self.white_king.possible_moves:
                if move not in self.black_moves:
                    checkmate = False 

            # Check if there is a piece that can block the path of the attacking_piece
            if self.path_to_king:
                for piece in self.black_pieces:
                    if piece.name[1] != 'K':
                        for move in piece.possible_moves:
                            if move in self.path_to_king:
                                checkmate = False
                            else:
                                piece.possible_moves.remove(move)
    
        return checkmate

    def getAttackingPiecePathToKing(self):
        if not self.attacking_piece: return

        if self.attacking_piece.color == "white":
            dx = self.black_king.row - self.attacking_piece.row
            dy = self.black_king.col - self.attacking_piece.col
            king_x, king_y = self.black_king.row, self.black_king.col
        else:
            dx = self.white_king.row - self.attacking_piece.row 
            dy = self.white_king.col - self.attacking_piece.col
            king_x, king_y = self.white_king.row, self.white_king.col

        path_to_king = []

        if self.attacking_piece.name[1] == 'R':
            step_x, step_y = (dx // abs(dx), 0) if dx != 0 else (0, dy // abs(dy))
        elif self.attacking_piece.name[1] == 'B':
            if abs(dx) == abs(dy):
                step_x, step_y = dx // abs(dx), dy // abs(dy)
            else:
                return path_to_king
        elif self.attacking_piece.name[1] == 'Q':
            if dx == 0 or dy == 0:
                step_x, step_y = (dx // abs(dx), 0) if dx != 0 else (0, dy // abs(dy))
            elif abs(dx) == abs(dy):
                step_x, step_y = dx // abs(dx), dy // abs(dy)
            else:
                return path_to_king
        else:
            return path_to_king

        current_x, current_y = self.attacking_piece.row + step_x, self.attacking_piece.col + step_y
        while (current_x, current_y) != (king_x, king_y):
            path_to_king.append((current_x, current_y))
            current_x, current_y = current_x + step_x, current_y + step_y

        return path_to_king

        
    def setMovesForAllPieces(self):
        self.white_moves = []
        self.black_moves = []

        for square in self.board_map.values():
            if square.piece:
                square.piece.board_map = self.board_map
                square.piece.setPossibleMoves()

                if square.piece.color == "white":
                    self.white_pieces.append(square.piece)
                else:
                    self.black_pieces.append(square.piece)

                for move in square.piece.possible_moves:
                    if square.piece.color == "white":
                        self.white_moves.append(move)
                    else:
                        self.black_moves.append(move)

    def draw(self):
        self.draw_board()
        self.draw_pieces()


class BoardSquare:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

        self.piece = None
