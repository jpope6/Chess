import pygame as pg
from const import *
import sys
from board import Board

class Game:
    def __init__(self):
        pg.init()
        self.size = HEIGHT, WIDTH
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Chess")

        self.board = Board(self.screen)

    def play(self):
        while True:
            self.screen.fill(BLACK)
            self.board.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    mouse_x = mouse_pos[0] // SQUARE_SIZE
                    mouse_y = mouse_pos[1] // SQUARE_SIZE

                    if (mouse_x, mouse_y) in self.board.board_map:
                        board_square = self.board.board_map[(mouse_x, mouse_y)]
                        if board_square.piece:
                            self.board.active_piece = board_square.piece;
                            self.board.active_piece.active = True
                        else:
                            if self.board.active_piece:
                                self.board.move(mouse_x, mouse_y)
        

            pg.display.update()


def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
