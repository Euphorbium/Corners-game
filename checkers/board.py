import pygame

from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, TABLE
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        reds = sum([TABLE[piece.col][piece.row] for piece in self.get_all_pieces(RED)])
        whites = sum([TABLE[piece.col][piece.row] * -1 for piece in self.get_all_pieces(WHITE)])
        return reds + whites

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col < 4:
                    if row < 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    if row >= 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def winner(self):
        top_corner = [self.board[row][col] for row in range(4) for col in range(4)]
        bottom_corner = [self.board[row][col] for row in range(4, 8) for col in range(4, 8)]
        if all(top_corner):
            if all([piece.color == RED for piece in top_corner]):
                return RED
        elif all(bottom_corner):
            if all([piece.color == WHITE for piece in bottom_corner]):
                return WHITE

        return None

    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row

        moves.update(self._traverse_left(row, piece.color, piece.col))
        moves.update(self._traverse_right(row, piece.color, piece.col))
        moves.update(self._traverse_up(row, piece.color, piece.col))
        moves.update(self._traverse_down(row, piece.color, piece.col))

        return moves

    def _traverse_left(self, row, color, column, previous=None):
        moves = {}

        if column < 0:
            return moves

        if not previous and column - 1 >= 0 and self.board[row][column - 1] == 0:
            moves[(row, column - 1)] = []
            return moves

        if not previous:
            previous = [(row, column)]
        else:
            previous += [(row, column)]

        # traverse left
        if column - 2 >= 0 and self.board[row][column - 1] and self.board[row][column - 2] == 0 \
                and (row, column - 2) not in previous:
            moves[(row, column - 2)] = previous
            moves.update(self._traverse_left(row, color, column - 2, previous=previous))
        # traverse up
        if row - 2 >= 0 and self.board[row - 1][column] and self.board[row - 2][column] == 0 \
                and (row - 2, column) not in previous:
            moves[(row - 2, column)] = previous
            moves.update(self._traverse_up(row - 2, color, column, previous=previous))
        # traverse down
        if row + 2 < ROWS and self.board[row + 1][column] and self.board[row + 2][column] == 0 \
                and (row + 2, column) not in moves:
            moves[(row + 2, column)] = previous
            moves.update(self._traverse_down(row + 2, color, column, previous=previous))
        return moves

    def _traverse_right(self, row, color, column, previous=None):
        moves = {}

        if column >= COLS:
            return moves

        if not previous and column < COLS - 1 and self.board[row][column + 1] == 0:
            moves[(row, column + 1)] = []
            return moves

        if not previous:
            previous = [(row, column)]
        else:
            previous += [(row, column)]

        # traverse right
        if column + 2 < COLS and self.board[row][column + 1] and self.board[row][column + 2] == 0 \
                and (row, column + 2) not in moves:
            moves[(row, column + 2)] = previous
            moves.update(self._traverse_right(row, color, column + 2, previous=previous))
        # traverse up
        if row - 2 >= 0 and self.board[row - 1][column] and self.board[row - 2][column] == 0 \
                and (row - 2, column) not in previous:
            moves[(row - 2, column)] = previous
            moves.update(self._traverse_up(row - 2, color, column, previous=previous))
        # traverse down
        if row + 2 < ROWS and self.board[row + 1][column] and self.board[row + 2][column] == 0 \
                and (row + 2, column) not in moves:
            moves[(row + 2, column)] = previous
            moves.update(self._traverse_down(row + 2, color, column, previous=previous))

        return moves

    def _traverse_up(self, row, color, column, previous=None):
        moves = {}

        if row < 0:
            return moves

        if not previous and row - 1 >= 0 and self.board[row - 1][column] == 0:
            moves[(row - 1, column)] = []
            return moves

        if not previous:
            previous = [(row, column)]
        else:
            previous += [(row, column)]

        # traverse left
        if column - 2 >= 0 and self.board[row][column - 1] and self.board[row][column - 2] == 0 \
                and (row, column - 2) not in previous:
            moves[(row, column - 2)] = previous
            moves.update(self._traverse_left(row, color, column - 2, previous=previous))

        # traverse right
        if column + 2 < COLS and self.board[row][column + 1] and self.board[row][column + 2] == 0 \
                and (row, column + 2) not in moves:
            moves[(row, column + 2)] = previous

            moves.update(self._traverse_right(row, color, column + 2, previous=previous))

        # traverse up
        if row - 2 >= 0 and self.board[row - 1][column] and self.board[row - 2][column] == 0 \
                and (row - 2, column) not in previous:
            moves[(row - 2, column)] = previous

            moves.update(self._traverse_up(row - 2, color, column, previous=previous))

        return moves

    def _traverse_down(self, row, color, column, previous=None):
        moves = {}

        if row >= ROWS:
            return moves

        if not previous and row + 1 < ROWS and self.board[row + 1][column] == 0:
            moves[(row + 1, column)] = []
            return moves

        if not previous:
            previous = [(row, column)]
        else:
            previous += [(row, column)]

        # traverse left
        if column - 2 >= 0 and self.board[row][column - 1] and self.board[row][column - 2] == 0 \
                and (row, column - 2) not in previous:
            moves[(row, column - 2)] = previous

            moves.update(self._traverse_left(row, color, column - 2, previous=previous))
        # traverse right
        if column + 2 < COLS and self.board[row][column + 1] and self.board[row][column + 2] == 0 \
                and (row, column + 2) not in moves:
            moves[(row, column + 2)] = previous

            moves.update(self._traverse_right(row, color, column + 2, previous=previous))
        # traverse down
        if row + 2 < ROWS and self.board[row + 1][column] and self.board[row + 2][column] == 0 \
                and (row + 2, column) not in moves:
            moves[(row + 2, column)] = previous

            moves.update(self._traverse_down(row + 2, color, column, previous=previous))

        return moves
