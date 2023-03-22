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

        self.turn = "white"

        self.white_moves = []
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
        if self.turn == "white":
            for move in self.white_moves:
                if move == (self.black_king.row, self.black_king.col):
                    print("check")
                    if self.checkForCheckmate():
                        print("checkmate")

        if self.turn == "black":
            for move in self.black_moves:
                if move == (self.white_king.row, self.white_king.col):
                    print("check")
                    if self.checkForCheckmate():
                        print("checkmate")

    def checkForCheckmate(self):
        if self.turn == "white":
            for move in self.black_king.possible_moves:
                if move not in self.white_moves:
                    return False

        if self.turn == "black":
            for move in self.white_king.possible_moves:
                if move not in self.black_moves:
                    return False 

        return True

    def setMovesForAllPieces(self):
        self.white_moves = []
        self.black_moves = []

        for square in self.board_map.values():
            if square.piece:
                square.piece.board_map = self.board_map
                square.piece.setPossibleMoves()

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
