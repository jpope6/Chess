import pygame as pg
import const
from piece import *

class Board():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.board = self.draw_board_array()

    def draw_board_array(self):
        board = [["" for j in range(8)] for i in range(8)]

        # pawns
        for i in range(8):
            board[i][6] = "WP"
            board[i][1] = "BP"

        board[1][0] = "BH"
        board[6][0] = "BH"
        board[1][7] = "WH"
        board[6][7] = "WH"

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

    def draw_pieces(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == "WP":
                    white_pawn = Pawn(self.screen, "WP", i, j)
                    white_pawn.draw()

                if self.board[i][j] == "BP":
                    black_pawn = Pawn(self.screen, "BP", i, j)
                    black_pawn.draw()

                if self.board[i][j] == "WH":
                    white_horse = Knight(self.screen, "WH", i, j)
                    white_horse.draw()

                if self.board[i][j] == "BH":
                    black_horse = Knight(self.screen, "BH", i, j)
                    black_horse.draw()

    def draw(self):
        self.draw_board()
        self.draw_pieces()
