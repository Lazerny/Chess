# скачать картинки: https://disk.yandex.ru/d/yBSyEyOMVCguwg
WHITE = 1
BLACK = 2
cords_black_king = (7, 4)
cords_white_king = (0, 4)

from stockfish import Stockfish

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


class Board:
    def __init__(self, color):
        if color == 1:
            self.color = WHITE
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
            self.color = WHITE
            self.field = []
            for row in range(8):
                self.field.append([None] * 8)
            self.field[7] = [
                Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
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
                Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
            ]

    # def __str__(self):
    #     return Main.print_board(board=self)

    def checkmate(self):
        row1 = 0
        col1 = 0
        if self.current_player_color() == WHITE:
            if self.cell(cords_white_king[0], cords_white_king[1]) == 'wK':
                row1, col1 = cords_white_king
            else:
                for i in range(8):
                    for j in range(8):
                        if self.cell(i, j) == 'wK':
                            change_cords_king(cords_white_king, i, j)
                            row1, col1 = cords_white_king
                            break
        elif self.cell(cords_black_king[0], cords_black_king[1]) == 'bK':
            row1, col1 = cords_black_king
        else:
            for i in range(8):
                for j in range(8):
                    if self.cell(i, j) == 'bK':
                        change_cords_king(cords_black_king, i, j)
                        row1, col1 = cords_black_king
                        break
        king = self.get_piece(row1, col1)
        if self.is_under_attack(row1, col1, opponent(king.get_color())):
            for i in range(row1 - 1, row1 + 3):
                for j in range(col1 - 1, col1 + 2):
                    if correct_coords(i, j):
                        if king.can_move(self, row1, col1, i, j):
                            return False
            all_shapes = self.is_under_attack(row1, col1, opponent(self.color))
            if len(all_shapes) > 1:
                return True
            for shape in all_shapes:
                row, col = all_shapes[shape]
                if not self.is_under_attack(row, col, self.color):
                    line = False
                    if shape.char() == 'Q':
                        step = 1 if (row1 >= row) else -1
                        for r in range(row, row1, step):
                            if r == row and col1 == col:
                                line = True
                                break
                        if line:
                            for r in range(row, row1, step):
                                if self.is_under_attack(r, col, self.color):
                                    return False
                            return True
                        step = 1 if (col1 >= col) else -1
                        for c in range(col, col1, step):
                            if c == col1 and row == row1:
                                line = True
                                break
                        if line:
                            for c in range(col, col1, step):
                                if self.is_under_attack(row, c, self.color):
                                    return False
                            return True
                        step_r = 1 if (row1 >= row) else -1
                        step_c = 1 if (col1 >= col) else -1
                        while c != col1 and r != row1:
                            if c == col and row == r:
                                line = True
                                break
                            c, r = c + step_c, r + step_r
                        if line:
                            while c != col1 and r != row1:
                                if self.is_under_attack(r, c, self.color):
                                    return False
                                c, r = c + step_c, r + step_r
                            return True

                    elif shape.char() == 'R':
                        step = 1 if (row1 >= row) else -1
                        for r in range(row, row1, step):
                            if r == row and col == col1:
                                line = True
                                break
                        if line:
                            for r in range(row, row1, step):
                                if self.is_under_attack(r, col, self.color):
                                    return False
                            return True

                        step = 1 if (col1 >= col) else -1
                        for c in range(col, col1, step):
                            if c == col1 and row == row1:
                                line = True
                                break
                        if line:
                            for c in range(col, col1, step):
                                if self.is_under_attack(row, c, self.color):
                                    return False
                            return True

                    elif shape.char() == 'B':
                        step = 1 if (row1 >= row) else -1
                        step1 = 1 if (col1 >= col) else -1
                        c = col + step1
                        for r in range(row, row1, step):
                            if row1 == r and c == col1:
                                line = True
                                break
                            c += step1
                        if line:
                            for r in range(row, row1, step):
                                if self.is_under_attack(r, c, self.color):
                                    return False
                                c += step1
                            return True

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

    def castling0(self):
        if self.current_player_color() == 1:
            r = self.get_piece(0, 0)
            k = self.get_piece(0, 4)
            if r is None or k is None:
                return False
            if r.get_color() == 1 and r.char() == 'R' and not r.do_move() \
                    and k.get_color() == 1 and k.char() == 'K' and not k.do_move() and \
                    not self.is_under_attack(0, 4, BLACK):
                for i in range(1, 4):
                    if not (self.get_piece(0, i) is None):
                        return False
                self.field[0][3] = self.field[0][0]
                self.field[0][2] = self.field[0][4]
                self.field[0][0] = None
                self.field[0][4] = None
                self.color = opponent(self.color)
                self.field[0][2].first_move()
                self.field[0][3].first_move()
                return True
            return False
        else:
            r = self.get_piece(7, 0)
            k = self.get_piece(7, 4)
            if r is None or k is None:
                return False
            if r.get_color() == 2 and r.char() == 'R' and not r.do_move() \
                    and k.get_color() == 2 and k.char() == 'K' and not k.do_move() and \
                    not self.is_under_attack(7, 4, WHITE):
                for i in range(1, 4):
                    if not (self.get_piece(7, i) is None):
                        return False
                self.field[7][3] = self.field[7][0]
                self.field[7][2] = self.field[7][4]
                self.field[7][0] = None
                self.field[7][4] = None
                self.color = opponent(self.color)
                self.field[7][3].first_move()
                self.field[7][2].first_move()
                return True
            return False

    def castling7(self):
        if self.current_player_color() == WHITE:
            r = self.get_piece(0, 7)
            k = self.get_piece(0, 4)
            if r is None or k is None:
                return False
            if r.get_color() == 1 and r.char() == 'R' and not r.do_move() \
                    and k.get_color() == 1 and k.char() == 'K' and not k.do_move() and \
                    not self.is_under_attack(0, 4, BLACK):
                for i in range(5, 7):
                    if not (self.get_piece(0, i) is None):
                        return False
                self.field[0][5] = self.field[0][7]
                self.field[0][6] = self.field[0][4]
                self.field[0][7] = None
                self.field[0][4] = None
                self.color = opponent(self.color)
                self.field[0][5].first_move()
                self.field[0][6].first_move()
                return True
            return False
        else:
            r = self.get_piece(7, 7)
            k = self.get_piece(7, 4)
            if r is None or k is None:
                return False
            if r.get_color() == 2 and r.char() == 'R' and not r.do_move() \
                    and k.get_color() == 2 and k.char() == 'K' and not k.do_move() and \
                    not self.is_under_attack(7, 4, WHITE):
                for i in range(5, 7):
                    if not (self.get_piece(7, i) is None):
                        return False
                self.field[7][5] = self.field[7][7]
                self.field[7][6] = self.field[7][4]
                self.field[7][7] = None
                self.field[7][4] = None
                self.color = opponent(self.color)
                self.field[7][5].first_move()
                self.field[7][6].first_move()
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
        if piece is None:  # если нет фигуры которую двигаем
            return False
        if piece.get_color() != self.color:  # если двигаем цвет фигуры что ходила
            return False

        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1): # если фигура не может сходить в клетку row1, col1
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1): # если не может съесть фигуру
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
        direction = 1 if (self.start_row == 1) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


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
                    elif i.char() == 'K' and i.get_color() == opponent(self.color):
                        if 0 <= abs(row2 - row1) <= 1 and 0 <= abs(col2 - col1) <= 1:
                            return False
                    elif i.get_color() == opponent(self.color) and i.can_attack(board, row2, col2, row1, col1):
                        return False

            piece = board.field[row][col]
            second_cell = board.field[row1][col1]
            if second_cell and piece:
                if board.field[row1][col1].get_color() != opponent(piece.get_color()):
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
