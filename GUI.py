import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QStatusBar, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEventLoop, QCoreApplication, QEvent
from PyQt5 import uic
from шахматы import Board, opponent


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.pieces = {}
        self.cord1 = (0, 0)
        self.cord2 = (0, 0)
        self.initUI()
        self.label_move_piece = 0

    def initUI(self):
        self.setWindowTitle('Шахматы')
        self.setMinimumSize(430, 430)  # Минимальный размер окна
        self.setMaximumSize(1044, 1044)  # Максимальный размер окна
        self.setGeometry(600, 30, 1044, 1044)  # Начальный размер окна

        self.piece_images = {
            'wQ': QPixmap('ChessImage/whiteQueen.png'),
            'wR': QPixmap('ChessImage/whiteRook.png'),
            'wN': QPixmap('ChessImage/whiteKnight.png'),
            'wB': QPixmap('ChessImage/whiteBishop.png'),
            'wK': QPixmap('ChessImage/whiteKing.png'),
            'wP': QPixmap('ChessImage/whitePawn.png'),
            'bQ': QPixmap('ChessImage/blackQueen.png'),
            'bR': QPixmap('ChessImage/blackRook.png'),
            'bN': QPixmap('ChessImage/blackKnight.png'),
            'bB': QPixmap('ChessImage/blackBishop.png'),
            'bK': QPixmap('ChessImage/blackKing.png'),
            'bP': QPixmap('ChessImage/blackPawn.png'),
        }

        #  Создаем QLabel для фонового изображения
        self.label_background = QLabel(self)
        self.pixmap_background = QPixmap('ChessImage/blue-marble.jpg')
        self.label_background.setPixmap(self.pixmap_background)
        self.label_background.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def start_and_get_info(self, color, login):
        self.board = Board(color)
        self.print_board(self.board)
        self.color = color
        self.login = login

    def resizeEvent(self, event):
        # масштабирование заднего фона(доски)
        self.label_background.setPixmap(self.pixmap_background.scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        smaller = min(self.width(), self.height())
        self.resize(smaller, smaller)

        # масштабирование фигур
        self.print_board(self.board)

    def get_cord_mouse(self, pos):
        cord_x = pos[0]
        cord_y = pos[1]
        step = self.width() // 8
        # print((7 - cord_y // step, cord_x // step))
        # row col
        return (7 - cord_y // step, cord_x // step)

    def mouseMoveEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        x, y = self.cord1
        dif_x = x - self.x
        dif_y = y - self.y
        if self.label_move_piece:
            self.label_move_piece.move(self.top_left_point_label[0] - dif_x, self.top_left_point_label[1] - dif_y)
        # print(self.x, self.y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.x = event.x()
            self.y = event.y()
            self.cord1 = (self.x, self.y)
            pos_in_board = self.get_cord_mouse(self.cord1)
            piece = self.board.cell(*pos_in_board)
            if piece != '  ':
                step = self.width() // 8
                self.top_left_point_label = step * pos_in_board[1], step * (7 - pos_in_board[0])
                # print('top_left_point_label:', self.top_left_point_label)
                name_move_piece = piece + ''.join(str(i) for i in self.get_cord_mouse(self.cord1))

                self.label_move_piece = self.pieces.get(name_move_piece)
                # print(f"cord1: {self.cord1}")
                # print(pos_in_board)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.cord2 = (self.x, self.y)
            # print(f"cord2: {self.cord2}")
            self.run()

    def print_board(self, board):
        for key in self.pieces:
            label = self.pieces.get(key)
            label.clear()

        cord_y = self.height()
        for row in range(8):
            cord_x = 0
            for col in range(8):
                cell = board.cell(row, col)
                if cell != '  ':
                    label = QLabel(self)
                    piece_name = cell + str(row) + str(col)
                    label.setPixmap(
                        self.piece_images[cell].scaledToWidth(self.width() // 8))
                    self.pieces[piece_name] = label
                    label.setGeometry(cord_x, cord_y - self.width() // 8, self.width() // 8, self.width() // 8 - 10)
                    label.show()

                cord_x += self.width() // 8
            cord_y -= self.height() // 8

    def run(self):
        row, col = self.get_cord_mouse(self.cord1)
        row1, col1 = self.get_cord_mouse(self.cord2)
        # print(row, col)
        # print(row1, col1)
        if row == 0 and col == 4 and row1 == 0 and col1 == 0:
            self.board.castling0()
        elif row == 7 and col == 4 and row1 == 7 and col1 == 0:
            self.board.castling0()
        elif row == 0 and col == 4 and row1 == 0 and col1 == 7:
            self.board.castling7()
        elif row == 7 and col == 4 and row1 == 7 and col1 == 7:
            self.board.castling7()
        elif row1 == 7 or row1 == 0:
            piece = self.board.field[row][col]
            if piece.char() == 'P' and self.board.move_piece(row, col, row1, col1):
                # print('Превращение на координате', row1, col1)
                color_who_promote = 'w' if opponent(self.board.color) == 1 else 'b'
                step = self.width() // 8
                top_left_point_x = step * col1
                top_left_point_y = step * (7 - row1)

                pixmaps_for_pieces_which_we_choose = {
                    'wQ': QPixmap('ChessImage/Choose_piece/whiteQueen.png'),
                    'wR': QPixmap('ChessImage/Choose_piece/whiteRook.png'),
                    'wN': QPixmap('ChessImage/Choose_piece/whiteKnight.png'),
                    'wB': QPixmap('ChessImage/Choose_piece/whiteBishop.png'),
                    'bQ': QPixmap('ChessImage/Choose_piece/blackQueen.png'),
                    'bR': QPixmap('ChessImage/Choose_piece/blackRook.png'),
                    'bN': QPixmap('ChessImage/Choose_piece/blackKnight.png'),
                    'bB': QPixmap('ChessImage/Choose_piece/blackBishop.png'),
                }
                names = [color_who_promote + 'Q',
                         color_who_promote + 'R',
                         color_who_promote + 'B',
                         color_who_promote + 'N']
                n = 0
                list_to_clear = []
                if row1 == 7:
                    for y in range(0, step * 4, step):
                        label = QLabel(self)
                        label.setPixmap(
                            pixmaps_for_pieces_which_we_choose.get(names[n]).scaledToWidth(self.width() // 8))
                        label.setGeometry(top_left_point_x, y, self.width() // 8, self.width() // 8)
                        list_to_clear.append(label)
                        label.show()
                        n += 1
                else:
                    for y in range(top_left_point_y, top_left_point_y - step * 4, -step):
                        label = QLabel(self)
                        label.setPixmap(
                            pixmaps_for_pieces_which_we_choose.get(names[n]).scaledToWidth(self.width() // 8))
                        label.setGeometry(top_left_point_x, y, self.width() // 8, self.width() // 8)
                        list_to_clear.append(label)
                        label.show()
                        n += 1

                choose_piese = False
                try:
                    while not choose_piese:
                        QApplication.processEvents()
                        mouse = self.get_cord_mouse(self.cord1)

                        piece_mapping = {
                            (7, col1): 'Q',
                            (6, col1): 'R',
                            (5, col1): 'B',
                            (4, col1): 'N',
                            (0, col1): 'Q',
                            (1, col1): 'R',
                            (2, col1): 'B',
                            (3, col1): 'N',
                        }

                        if mouse in piece_mapping:
                            for i in list_to_clear:
                                i.clear()
                            char = piece_mapping[mouse]
                            choose_piese = True
                except Exception as e:
                    print(e)

                self.board.promote_pawn(row1, col1, char)

        self.board.move_piece(row, col, row1, col1)
        self.print_board(self.board)
        if self.board.checkmate():
            try:
                db = DatabaseManager()
                query = '''SELECT user_id FROM Users WHERE user = ?'''
                params = (self.login,)
                user_id = db.execute_query(query, params)
                user_id = user_id[0][0]
                if self.board.color == self.color:
                    query = '''UPDATE Information 
    SET rating = (SELECT rating FROM Information WHERE id = ?) - 30
    WHERE id = ?;
    '''
                    params = (user_id, user_id)
                    db.execute_query(query, params)
                else:
                    query = '''UPDATE Information 
    SET rating = (SELECT rating FROM Information WHERE id = ?) + 30
    WHERE id = ?;
    '''
                    params = (user_id, user_id)
                    db.execute_query(query, params)
            except Exception as e:
                print(e)
            print('Checkmate!')


class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('first window.ui', self)
        self.playWithFriend.clicked.connect(self.play_with_friend_def)
        self.playWithBot.clicked.connect(self.play_with_bot_def)
        self.reference.clicked.connect(self.reference_def)
        self.setFixedSize(self.width(), self.height())

    def play_with_friend_def(self):
        self.hide()
        sw.show()

    def play_with_bot_def(self):
        self.hide()
        sw.show()

    def reference_def(self):
        r.show()


class Reference(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        rules_text = self.load_rules_from_file("reference.txt")
        rules_label = QLabel(rules_text)
        layout.addWidget(rules_label)
        self.setLayout(layout)
        self.setWindowTitle('Правила игры')
        self.setGeometry(100, 100, 400, 300)

    def load_rules_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                rules_text = file.read()
            return rules_text
        except FileNotFoundError:
            return "Файл с правилами не найден."


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.login_user = ''
        self.password_user = ''

    def initUI(self):
        uic.loadUi('second window.ui', self)
        self.status_bar = QStatusBar(self)
        self.status_bar.setGeometry(0, self.height() - 25, self.width(), 25)
        self.setFixedSize(self.width(), self.height())
        self.pushButton.clicked.connect(self.run)

    def run(self, color):
        try:
            if not self.login.text() and not self.password.text():
                # self.status_bar.setVisible(True)
                self.status_bar.showMessage('Введите своё имя и приудмайте пароль!')
            elif not self.password.text():
                self.status_bar.showMessage('Введите пароль!')
            elif not self.login.text():
                self.status_bar.showMessage('Введите своё имя!')
            else:
                self.status_bar.showMessage('')
                db = DatabaseManager()
                query = '''SELECT user_id FROM USERS WHERE user = ?'''
                params = (self.login.text(),)
                user_id = db.execute_query(query, params)

                if user_id:
                    query = '''SELECT password FROM INFORMATION WHERE id = ?'''
                    params = (user_id[0][0],)
                    if db.execute_query(query, params)[0][0] != self.password.text():
                        self.status_bar.showMessage('Неправильный пароль к аккаунту')
                        return
                    else:
                        self.login_user = self.login.text()
                        self.password_user = self.password.text()

                        self.hide()
                        color = 1 if self.White.isChecked() else 2
                        mw.start_and_get_info(color, self.login.text())
                        mw.show()
                        return

                query = """INSERT INTO Users (user) values (?)"""
                params = (self.login.text(),)
                db.execute_query(query, params)
                query = """INSERT INTO Information (id, password)
    VALUES ((SELECT user_id FROM Users WHERE user = ?), ?);"""
                params = (self.login.text(), self.password.text())
                db.execute_query(query, params)
                self.login_user = self.login.text()
                self.password_user = self.password.text()

                color = 1 if self.White.isChecked() else 2
                self.hide()
                mw.start_and_get_info(color, self.login.text())
                mw.show()
        except Exception as e:
            print(e)


class DatabaseManager:
    def __init__(self, db_name='Chess.sqlite'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            if params:
                result = self.cursor.execute(query, params).fetchall()
            else:
                result = self.cursor.execute(query)
            self.conn.commit()
            return result

        except Exception as e:
            print(e)

    def fetch_data(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fw = FirstWindow()  # First window
    sw = SecondWindow()  # Second window
    mw = Main()  # Main window
    r = Reference()  # Reference
    sw.show()
    sys.exit(app.exec_())
