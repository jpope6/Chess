import pygame as pg
import const
import sys
from board import Board

class Game:
    def __init__(self):
        pg.init()
        self.size = const.HEIGHT, const.WIDTH
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Chess")

        self.board = Board(self.screen)

    def play(self):
        while True:
            self.screen.fill(const.BLACK)
            self.board.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

            pg.display.update()


def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
