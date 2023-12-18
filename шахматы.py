from stockfish import Stockfish
import chess

# скачать картинки: https://disk.yandex.ru/d/yBSyEyOMVCguwg
WHITE = 1
BLACK = 2
cords_black_king = (7, 4)
cords_white_king = (0, 4)


def change_cords_king(var, i, j):
    global cords_black_king
    global cords_white_king
    if var == cords_black_king:
        cords_black_king = (i, j)
    else:
        cords_white_king = (i, j)


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class Bot:
    def __init__(self, level):
        self.stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe")
        self.stockfish.set_skill_level(level)
        self.stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def get_best_move(self):
        return self.stockfish.get_best_move()

    def update_position(self, move):
        self.stockfish.make_moves_from_current_position([move])


class Board:
    def __init__(self, color):
        self.color = WHITE
        self.board_for_track_end = chess.Board()
        if color == 1:
            self.field = []
            for row in range(8):
                self.field.append([None] * 8)
            self.field[0] = [
                Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
            ]
            self.field[1] = [
                Pawn(WHITE, 1), Pawn(WHITE, 1), Pawn(WHITE, 1), Pawn(WHITE, 1),
                Pawn(WHITE, 1), Pawn(WHITE, 1), Pawn(WHITE, 1), Pawn(WHITE, 1)
            ]
            self.field[6] = [
                Pawn(BLACK, 6), Pawn(BLACK, 6), Pawn(BLACK, 6), Pawn(BLACK, 6),
                Pawn(BLACK, 6), Pawn(BLACK, 6), Pawn(BLACK, 6), Pawn(BLACK, 6)
            ]
            self.field[7] = [
                Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
            ]
        else:
            self.field = []
            for row in range(8):
                self.field.append([None] * 8)
            self.field[7] = [
                Rook(WHITE), Knight(WHITE), Bishop(WHITE), King(WHITE),
                Queen(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
            ]
            self.field[6] = [
                Pawn(WHITE, 6), Pawn(WHITE, 6), Pawn(WHITE, 6), Pawn(WHITE, 6),
                Pawn(WHITE, 6), Pawn(WHITE, 6), Pawn(WHITE, 6), Pawn(WHITE, 6)
            ]
            self.field[1] = [
                Pawn(BLACK, 1), Pawn(BLACK, 1), Pawn(BLACK, 1), Pawn(BLACK, 1),
                Pawn(BLACK, 1), Pawn(BLACK, 1), Pawn(BLACK, 1), Pawn(BLACK, 1)
            ]
            self.field[0] = [
                Rook(BLACK), Knight(BLACK), Bishop(BLACK), King(BLACK),
                Queen(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
            ]

    # def __str__(self):
    #     return Main.print_board(board=self)

    def checkmate(self):
        # 1 Атаковано ли поле с королём? Если нет, то не мат.
        # 2 Атакованы ли соседние с королём и свободные от его фигур поля? Если нет, то не мат.
        # 3 Сколько фигур атакуют короля? Если две, то мат.
        # 4 Можно ли съесть атакующую фигуру? Если да, то не мат.
        # 5 Атакует конь? Если да, то мат.
        # 6 Атакующая фигура на соседнем поле? Если да, то мат.
        # 7 Можно ли перекрыть линию атаки? Если да, то не мат. Иначе - мат.
        return self.board_for_track_end.is_checkmate()

    def stalemate(self):
        return self.board_for_track_end.is_stalemate()

    def is_insufficient_material(self):
        return self.board_for_track_end.is_insufficient_material()

    def check(self):
        if self.color == WHITE:
            if self.cell(cords_white_king[0], cords_white_king[1]) == 'wK':
                if self.is_under_attack(cords_white_king[0], cords_white_king[1], BLACK):
                    return True
            else:
                for i in range(8):
                    for j in range(8):
                        if self.cell(i, j) == 'wK':
                            change_cords_king(cords_white_king, i, j)
                            if self.is_under_attack(cords_white_king[0], cords_white_king[1], BLACK):
                                return True

        elif self.cell(cords_black_king[0], cords_black_king[1]) == 'bK':
            if self.is_under_attack(cords_black_king[0], cords_black_king[1], WHITE):
                return True
        else:
            for i in range(8):
                for j in range(8):
                    if self.cell(i, j) == 'bK':
                        change_cords_king(cords_black_king, i, j)
                        if self.is_under_attack(cords_black_king[0], cords_black_king[1], WHITE):
                            return True
        return False

    def castling_long(self, correct_row, col_king, col_rook):
        # print('0-0-0')
        r = self.get_piece(correct_row, col_rook)
        k = self.get_piece(correct_row, col_king)
        if r is None or k is None:
            return False
        if r.get_color() == k.get_color() and r.char() == 'R' and not r.do_move() \
                and k.char() == 'K' and not k.do_move():

            if col_rook > col_king:
                step = -1
                col_rook_for_loop = col_rook + step
            else:
                step = 1
                col_rook_for_loop = col_rook + step

            # Не мешают ли фигуры?
            for i in range(col_rook_for_loop, col_king, step):
                if not (self.get_piece(correct_row, i) is None):
                    return False

            # Не находится ли путь короля под боем?
            for cell in range(col_rook_for_loop + step, col_king + step, step):
                if self.is_under_attack(correct_row, cell, opponent(k.get_color())):
                    return False
            # Рокировка
            self.field[correct_row][col_king - step] = self.field[correct_row][col_rook]  # rook
            self.field[correct_row][col_rook_for_loop + step] = self.field[correct_row][col_king]  # king
            self.field[correct_row][col_rook] = None
            self.field[correct_row][col_king] = None
            self.color = opponent(self.color)
            self.field[correct_row][col_rook_for_loop + step].first_move()
            self.field[correct_row][col_king - step].first_move()
            if self.color == 1:  # рокировка черных
                queen_side_castle = chess.Move.from_uci("e8c8")
                self.board_for_track_end.push(queen_side_castle)
            else:  # рокировка белых
                queen_side_castle = chess.Move.from_uci("e1c1")
                self.board_for_track_end.push(queen_side_castle)
            return True
        return False

    def castling_short(self, correct_row, col_king, col_rook):
        # print('0-0')
        r = self.get_piece(correct_row, col_rook)
        k = self.get_piece(correct_row, col_king)
        if r is None or k is None:
            return False
        if r.get_color() == k.get_color() and r.char() == 'R' and not r.do_move() \
                and k.char() == 'K' and not k.do_move():

            if col_rook < col_king:
                step = -1
                col_rook_for_loop = col_rook - step
            else:
                step = 1
                col_rook_for_loop = col_rook - step

            # Не мешают ли фигуры?
            for i in range(col_king + step, col_rook, step):
                if not (self.get_piece(correct_row, i) is None):
                    return False

            # Не находится ли путь короля под боем?
            for cell in range(col_king, col_rook, step):
                if self.is_under_attack(correct_row, cell, opponent(k.get_color())):
                    return False
            # Рокировка
            self.field[correct_row][col_rook_for_loop - step] = self.field[correct_row][col_rook]  # rook
            self.field[correct_row][col_rook_for_loop] = self.field[correct_row][col_king]  # king
            self.field[correct_row][col_rook] = None
            self.field[correct_row][col_king] = None
            self.color = opponent(self.color)
            self.field[correct_row][col_rook_for_loop - step].first_move()
            self.field[correct_row][col_rook_for_loop].first_move()
            if self.color == 1:  # рокировка черных
                king_side_castle = chess.Move.from_uci("e8g8")
                self.board_for_track_end.push(king_side_castle)
            else:  # рокировка белых
                king_side_castle = chess.Move.from_uci("e1g1")
                self.board_for_track_end.push(king_side_castle)
            return True
        return False

    def promote_pawn(self, row1, col1, char):
        if char == 'Q':
            self.field[row1][col1] = Queen(opponent(self.color))
        elif char == 'R':
            self.field[row1][col1] = Rook(opponent(self.color))
        elif char == 'B':
            self.field[row1][col1] = Bishop(opponent(self.color))
        elif char == 'N':
            self.field[row1][col1] = Knight(opponent(self.color))
        return True

    def is_under_attack(self, row1, col1, color):
        res = {}
        for row, q in enumerate(self.field):
            for col, i in enumerate(q):
                if i is None:
                    ...
                elif i.get_color() == color and i.can_attack(self, row, col, row1, col1):
                    res[i] = (row, col)
        return res if res else False

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False"""
        # print('run "move_piece" function')
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:  # если нет фигуры, которую двигаем
            return False
        if piece.get_color() != self.color:  # если двигаем цвет фигуры, что ходила
            return False

        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):  # если фигура не может сходить в клетку row1, col1
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):  # если не может съесть фигуру
                return False
        else:
            return False

        self.field[row][col] = None  # Снять фигуру.
        step = self.field[row1][col1]
        self.field[row1][col1] = piece  # Поставить на новое место.
        if self.check():
            self.field[row][col] = piece
            self.field[row1][col1] = step
            # sound_check_continue.play()
            return False
        self.color = opponent(self.color)
        if self.checkmate():
            # sound_checkmate.play()
            # print(self.color)
            # print('Checkmate!')
            pass
        if piece.char() == 'R' or piece.char() == 'K':
            piece.first_move()
        return True


class Rook:

    def __init__(self, color):
        self.color = color
        self.movvee = False

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def first_move(self):
        self.movvee = True

    def do_move(self):
        return self.movvee

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row == row1 and col == col1:
            return False
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color, start_row):
        self.color = color
        self.start_row = start_row

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.start_row == 1:
            direction = 1
        else:
            direction = -1

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == self.start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        if board.field[row1][col1] is not None:
            direction = 1 if (self.start_row == 1) else -1
            return (row + direction == row1
                    and (col + 1 == col1 or col - 1 == col1))
        else:
            return False


class Knight:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        if abs(row - row1) == 2 and abs(col - col1) == 1 \
                or abs(row - row1) == 1 and abs(col - col1) == 2:
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:

    def __init__(self, color):
        self.color = color
        self.movvee = False

    def get_color(self):
        return self.color

    def first_move(self):
        self.movvee = True

    def do_move(self):
        return self.movvee

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if (0 <= abs(row - row1) <= 1 and 0 <= abs(col - col1) <= 1):
            for row2, q in enumerate(board.field):
                for col2, i in enumerate(q):

                    if i is None:
                        ...
                    elif i.char() == 'K' and i.get_color() == opponent(self.color):  # защита от бесконечного цикла
                        if 0 <= abs(row2 - row1) <= 1 and 0 <= abs(col2 - col1) <= 1:
                            return False
                    elif i.get_color() == opponent(self.color) and i.can_attack(board, row2, col2, row1, col1):
                        return False

            second_cell = board.field[row1][col1]
            if second_cell:
                if second_cell.get_color() == self.color:
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    """Класс ферзя."""

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if col == col1 and row != row1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            return True
        elif row == row1 and col != col1:
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True
        elif abs(row - row1) == abs(col - col1) and abs(row - row1) != 0:
            step_r = 1 if (row1 >= row) else -1
            step_c = 1 if (col1 >= col) else -1
            c, r = col + step_c, row + step_r
            while c != col1 and r != row1:
                if not (board.get_piece(r, c) is None):
                    return False
                c, r = c + step_c, r + step_r
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if abs(row - row1) == abs(col - col1):
            step = 1 if (row1 >= row) else -1
            step1 = 1 if (col1 >= col) else -1
            c = col + step1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, c) is None):
                    return False
                c += step1
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
