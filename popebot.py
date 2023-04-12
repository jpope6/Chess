import chess
import chess.polyglot

class Popebot:
    def __init__(self, board, color) -> None:
        self.board = board
        self.color = color
        self.depth = 3

        self.opening_book = "./assets/files/books/gm2600.bin"

    def is_endgame(self):
        # We should define where the ending begins. For me it might be either if:
        #   Both sides have no queens or
        #   Every side which has a queen has additionally no other pieces or one minorpiece maximum.

        queens = 0
        minor_piece = 0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            if piece and piece.piece_type == chess.QUEEN:
                queens += 1
            if piece and (piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT):
                minor_piece += 1

        return queens == 0 or (queens == 2 and minor_piece <= 1)

    def evaluate_mobility(self):
        score = 0
        for move in self.board.legal_moves:
            if self.board.turn == chess.WHITE:
                score += 1
            else:
                score -= 1
        return score

    def evaluate_pawn_structure(self):
        score = 0
        doubled_pawns = [0] * 8
        isolated_pawns = [0] * 8
    
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
    
            if piece and piece.piece_type == chess.PAWN:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
    
                # Doubled pawns
                if doubled_pawns[file]:
                    if piece.color == chess.WHITE:
                        score -= 50
                    else:
                        score += 50
                else:
                    doubled_pawns[file] = 1
    
                # Isolated pawns
                if file == 0:
                    if not isolated_pawns[file + 1]:
                        if piece.color == chess.WHITE:
                            score -= 25
                        else:
                            score += 25
                elif file == 7:
                    if not isolated_pawns[file - 1]:
                        if piece.color == chess.WHITE:
                            score -= 25
                        else:
                            score += 25
                else:
                    if not isolated_pawns[file - 1] and not isolated_pawns[file + 1]:
                        if piece.color == chess.WHITE:
                            score -= 25
                        else:
                            score += 25

                # Passed pawns
                passed = True
                for rank_offset in range(1, 8 - rank if piece.color == chess.WHITE else rank):
                    square_forward = square + rank_offset * (8 if piece.color == chess.WHITE else -8)
                    if self.board.piece_at(square_forward) and self.board.piece_at(square_forward).color != piece.color:
                        passed = False
                        break
        
    
                if passed:
                    if piece.color == chess.WHITE:
                        score += 100 - rank * 10
                    else:
                        score -= 100 - (7 - rank) * 10
    
        return score


    def evaluate_board(self):
        piece_values = {
        'P': -100, 'N': -320, 'B': -330, 'R': -500, 'Q': -900, 'K': -20000,
        'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000,}

    # Piece square tables for better piece positioning
        pawn_table = [
             0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
             5,  5, 10, 25, 25, 10,  5,  5,
             0,  0,  0, 20, 20,  0,  0,  0,
             5, -5,-10,  0,  0,-10, -5,  5,
             5, 10, 10,-20,-20, 10, 10,  5,
             0,  0,  0,  0,  0,  0,  0,  0
        ]

        knight_table = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ]

        bishop_table = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ]

        rook_table = [
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             0,  0,  0,  5,  5,  0,  0,  0
        ]

        king_table = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
             20, 20,  0,  0,  0,  0, 20, 20,
             20, 30, 10,  0,  0, 10, 30, 20
        ]

        king_endgame_table = [
            -50,-40,-30,-20,-20,-30,-40,-50,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -50,-30,-30,-30,-30,-30,-30,-50
        ]

        queen_table = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
             -5,  0,  5,  5,  5,  5,  0, -5,
              0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]

        evaluation = self.evaluate_mobility() + self.evaluate_pawn_structure() + self.evaluate_mobility()

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.symbol()]

                evaluation += value

                if piece.piece_type == chess.PAWN:
                    if piece.color == chess.WHITE:
                        evaluation += pawn_table[square]
                    else:
                        evaluation -= pawn_table[chess.square_mirror(square)]

                if piece.piece_type == chess.KNIGHT:
                    if piece.color == chess.WHITE:
                        evaluation += knight_table[square]
                    else:
                        evaluation -= knight_table[chess.square_mirror(square)]

                if piece.piece_type == chess.BISHOP:
                    if piece.color == chess.WHITE:
                        evaluation += bishop_table[square]
                    else:
                        evaluation -= bishop_table[chess.square_mirror(square)]

                if piece.piece_type == chess.ROOK:
                    if piece.color == chess.WHITE:
                        evaluation += rook_table[square]
                    else:
                        evaluation -= rook_table[chess.square_mirror(square)]
            
                if piece.piece_type == chess.KING:
                     if self.is_endgame():
                         if piece.color == chess.WHITE:
                             evaluation += king_endgame_table[square]
                         else:
                             evaluation -= king_endgame_table[chess.square_mirror(square)]
                     else:
                         if piece.color == chess.WHITE:
                             evaluation += king_table[square]
                         else:
                             evaluation -= king_table[chess.square_mirror(square)]

                if piece.piece_type == chess.QUEEN:
                    if piece.color == chess.WHITE:
                        evaluation += queen_table[square]
                    else:
                        evaluation -= queen_table[chess.square_mirror(square)]

        return evaluation

    def mva_lva_hueristic(self):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }


        moves = list(self.board.legal_moves)
        
        moves.sort(key=lambda move:

                   piece_values.get(self.board.piece_at(move.to_square).piece_type, 0) if self.board.piece_at(move.to_square) else 0
                   - 
                   piece_values.get(self.board.piece_at(move.from_square).piece_type, 0) if self.board.piece_at(move.from_square) else 0,
                   reverse=True)

        return moves
 

# Use A *???

    def minimax(self, depth, is_maximizing_player, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        legal_moves = self.mva_lva_hueristic()

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, not is_maximizing_player, alpha, beta)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, not is_maximizing_player, alpha, beta)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, depth):
        # First, check if there's a move in the opening book
        with chess.polyglot.open_reader(self.opening_book) as reader:
            try:
                opening_move = reader.weighted_choice(self.board).move
                return opening_move
            except IndexError:
                # No opening book move found, continue with your search algorithm
                pass


        best_move = None
        best_eval = float('-inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            eval = self.minimax(depth - 1, False, float('-inf'), float('inf'))
            self.board.pop()
            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move
