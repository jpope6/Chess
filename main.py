import pygame as pg
import chess
from const import *
import sys

class Game:
    def __init__(self):
        pg.init()
        self.size = HEIGHT, WIDTH
        self.screen = pg.display.set_mode(size=self.size)
        pg.display.set_caption("Chess")

        self.board = chess.Board()
        self.board_map = {}
        self.pieces = {}
        self.get_pieces()

        self.active_piece = None
        self.active_piece_square = -1


    def get_full_piece_name(self, piece):
        piece_name_map = {
            'P': 'pawn',
            'N': 'knight',
            'B': 'bishop',
            'R': 'rook',
            'Q': 'queen',
            'K': 'king',
        }
        piece_color = "white" if piece.color == chess.WHITE else "black"
        return piece_color + "_" + piece_name_map[piece.symbol().upper()]


    def get_pieces(self):
        for piece in chess.PIECE_NAMES:
            for color in chess.COLORS:
                if piece:
                    if color == chess.WHITE:
                        name = "white_" + piece
                    else:
                        name = "black_" + piece
                    image = pg.image.load(f"assets/images/{name}.png")
                    image = pg.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                    self.pieces[f"{name}"] = image


    def square_to_row(self, square):
        return chess.square_rank(square)

    def square_to_col(self, square):
        return chess.square_file(square)


    def draw_legal_moves(self, piece_square):
        if not self.active_piece: return

        legal_moves = [move for move in self.board.legal_moves if move.from_square == piece_square]

        for move in legal_moves:
            to_square = chess.square_mirror(move.to_square)
            row, col = self.square_to_row(to_square), self.square_to_col(to_square)
            rect = pg.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pg.draw.rect(self.screen, GREEN, rect, 3)


    def draw_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = LIGHT_COLOR
                else:
                    color = DARK_COLOR

                pg.draw.rect(self.screen, color, [
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE, 
                    SQUARE_SIZE,
                    SQUARE_SIZE
                    ])

                piece = self.board.piece_at(chess.square_mirror(row * 8 + col))
                self.board_map[chess.square_mirror(row * 8 + col)] = piece
                if piece:
                    piece_name = self.get_full_piece_name(piece)

                    self.screen.blit(self.pieces[piece_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))


    def play(self):
        while True:
            self.screen.fill(BLACK)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    mouse_x = mouse_pos[0] // SQUARE_SIZE
                    mouse_y = mouse_pos[1] // SQUARE_SIZE
                    piece = self.board.piece_at(chess.square_mirror(mouse_y * 8 + mouse_x))

                    if piece and piece.color == self.board.turn:
                        self.active_piece = piece
                        self.active_piece_square = chess.square_mirror(mouse_y * 8 + mouse_x)
                    else:
                        self.active_piece = None

            self.draw_board()
            self.draw_legal_moves(self.active_piece_square)
            pg.display.update()


def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
