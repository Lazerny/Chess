from database import DatabaseManager
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QStatusBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
from шахматы import Board, opponent, Bot


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
        f = open('theme.txt', 'r')
        self.root = f.read().split()
        f.close()
        self.piece_images = {
            'wQ': QPixmap(f'ChessImage/{self.root[0]}/wQ.png'),
            'wR': QPixmap(f'ChessImage/{self.root[0]}/wR.png'),
            'wN': QPixmap(f'ChessImage/{self.root[0]}/wN.png'),
            'wB': QPixmap(f'ChessImage/{self.root[0]}/wB.png'),
            'wK': QPixmap(f'ChessImage/{self.root[0]}/wK.png'),
            'wP': QPixmap(f'ChessImage/{self.root[0]}/wP.png'),
            'bQ': QPixmap(f'ChessImage/{self.root[0]}/bQ.png'),
            'bR': QPixmap(f'ChessImage/{self.root[0]}/bR.png'),
            'bN': QPixmap(f'ChessImage/{self.root[0]}/bN.png'),
            'bB': QPixmap(f'ChessImage/{self.root[0]}/bB.png'),
            'bK': QPixmap(f'ChessImage/{self.root[0]}/bK.png'),
            'bP': QPixmap(f'ChessImage/{self.root[0]}/bP.png'),
        }

        #  Создаем QLabel для фонового изображения
        self.label_background = QLabel(self)
        self.pixmap_background = QPixmap(f'ChessImage/{self.root[1]}/marble.png')
        self.label_background.setPixmap(self.pixmap_background)
        self.label_background.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def start_and_get_info(self, color, login, play_with_bot, level_bot):
        self.play_with_bot = play_with_bot
        if self.play_with_bot:
            self.bot = Bot(level_bot)
        self.board = Board(color)
        self.print_board(self.board)
        self.color = color
        self.login = login

    def change_design(self):
        f = open('theme.txt', 'r')
        self.root = f.read().split()
        f.close()
        self.piece_images = {
            'wQ': QPixmap(f'ChessImage/{self.root[0]}/wQ.png'),
            'wR': QPixmap(f'ChessImage/{self.root[0]}/wR.png'),
            'wN': QPixmap(f'ChessImage/{self.root[0]}/wN.png'),
            'wB': QPixmap(f'ChessImage/{self.root[0]}/wB.png'),
            'wK': QPixmap(f'ChessImage/{self.root[0]}/wK.png'),
            'wP': QPixmap(f'ChessImage/{self.root[0]}/wP.png'),
            'bQ': QPixmap(f'ChessImage/{self.root[0]}/bQ.png'),
            'bR': QPixmap(f'ChessImage/{self.root[0]}/bR.png'),
            'bN': QPixmap(f'ChessImage/{self.root[0]}/bN.png'),
            'bB': QPixmap(f'ChessImage/{self.root[0]}/bB.png'),
            'bK': QPixmap(f'ChessImage/{self.root[0]}/bK.png'),
            'bP': QPixmap(f'ChessImage/{self.root[0]}/bP.png'),
        }
        self.pixmap_background = QPixmap(f'ChessImage/{self.root[1]}/marble.png')
        self.label_background.setPixmap(self.pixmap_background)
        self.label_background.setAlignment(Qt.AlignTop | Qt.AlignLeft)

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
            if self.color != self.board.color and self.play_with_bot:
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

    def handle_castling(self, row, col, row1, col1, move):
        def update_pos():
            if self.play_with_bot:
                self.bot.update_position(move)

        if self.color == 1:
            if (row == 0 and col == 4 and row1 == 0 and col1 == 2) or (
                    row == 7 and col == 4 and row1 == 7 and col1 == 2):
                if self.board.castling_long(row, 4, 0):
                    update_pos()
            elif (row == 0 and col == 4 and row1 == 0 and col1 == 6) or (
                    row == 7 and col == 4 and row1 == 7 and col1 == 6):
                if self.board.castling_short(row, 4, 7):
                    update_pos()
        else:
            if (row == 0 and col == 3 and row1 == 0 and col1 == 5) or (
                    row == 7 and col == 3 and row1 == 7 and col1 == 5):
                if self.board.castling_long(row, 3, 7):
                    update_pos()
            elif (row == 0 and col == 3 and row1 == 0 and col1 == 1) or (
                    row == 7 and col == 3 and row1 == 7 and col1 == 1):
                if self.board.castling_short(row, 3, 0):
                    update_pos()

    def handle_bot_move(self, col_names_rev):
        move = self.bot.get_best_move()
        cell1 = move[:2]
        cell2 = move[2:4]
        if self.color == 1:
            col = col_names_rev.get(cell1[0])
            col1 = col_names_rev.get(cell2[0])
            row = int(cell1[1]) - 1
            row1 = int(cell2[1]) - 1
        else:
            col = 7 - col_names_rev.get(cell1[0])
            col1 = 7 - col_names_rev.get(cell2[0])
            row = 8 - int(cell1[1])
            row1 = 8 - int(cell2[1])
        return row, col, row1, col1, move

    def handle_human_move(self, col_names):
        row, col = self.get_cord_mouse(self.cord1)
        row1, col1 = self.get_cord_mouse(self.cord2)
        if self.color == 1:
            move = f"{col_names[col]}{row + 1}{col_names[col1]}{row1 + 1}"
        else:
            move = f"{col_names[7 - col]}{8 - row}{col_names[7 - col1]}{8 - row1}"
        return row, col, row1, col1, move

    def run(self):
        names_col = {0: 'a',
                     1: 'b',
                     2: 'c',
                     3: 'd',
                     4: 'e',
                     5: 'f',
                     6: 'g',
                     7: 'h'}

        names_col_rew = {'a': 0,
                         'b': 1,
                         'c': 2,
                         'd': 3,
                         'e': 4,
                         'f': 5,
                         'g': 6,
                         'h': 7}
        if self.color != self.board.color and self.play_with_bot:
            row, col, row1, col1, move = self.handle_bot_move(names_col_rew)
        else:
            row, col, row1, col1, move = self.handle_human_move(names_col)
        self.handle_castling(row, col, row1, col1, move)
        # promote pawn
        if row1 == 7 or row1 == 0:
            piece = self.board.field[row][col]
            if piece:
                if piece.char() == 'P' and self.board.move_piece(row, col, row1, col1):
                    # print('Превращение на координате', row1, col1)
                    color_who_promote = 'w' if opponent(self.board.color) == 1 else 'b'
                    if self.color == self.board.color and self.play_with_bot:  # Если это бот
                        self.bot.update_position(move)
                        # print(move[2:4])
                        char = self.bot.stockfish.get_what_is_on_square(move[2:4]).value.upper()

                    else:
                        step = self.width() // 8
                        top_left_point_x = step * col1
                        top_left_point_y = step * (7 - row1)

                        pixmaps_for_pieces_which_we_choose = {
                            'wQ': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/wQ.png'),
                            'wR': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/wR.png'),
                            'wN': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/wN.png'),
                            'wB': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/wB.png'),
                            'bQ': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/bQ.png'),
                            'bR': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/bR.png'),
                            'bN': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/bN.png'),
                            'bB': QPixmap(f'ChessImage/{self.root[0]}/Choose_piece/bB.png'),
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
                        if self.play_with_bot:
                            self.bot.update_position(move + char.lower())
                    # print(char.lower())
                    # print(move + char.lower())
                    self.board.board_for_track_end.push_san(move + char)
                    self.board.promote_pawn(row1, col1, char)
        # update position
        if self.board.move_piece(row, col, row1, col1):
            self.board.board_for_track_end.push_san(move)
            # print(self.board.board_for_track_end)
            if self.play_with_bot:
                self.bot.update_position(move)
                # print(self.bot.stockfish.get_board_visual(perspective_white=True))

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
            cm.show()
            # print('Checkmate!')

        if self.board.stalemate() or self.board.is_insufficient_material():
            sm.show()


class ChoosePiecesDesign(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('choose pieces design.ui', self)
        self.pushButton.clicked.connect(self.change_pieces_1)
        self.pushButton_2.clicked.connect(self.change_pieces_2)
        self.get_back.clicked.connect(self.back)
        self.setFixedSize(self.width(), self.height())
        self.label.setPixmap(QPixmap('ChessImage/cburnett/bN.png'))
        self.label_2.setPixmap(QPixmap('ChessImage/riohacha/bN.png'))

    def change_pieces_1(self):
        with open('theme.txt', 'r', encoding='utf-8', ) as f:
            data = f.read()
        board = data.split()[-1]
        with open('theme.txt', 'w', encoding='utf-8', ) as f:
            f.write('cburnett ' + board)
        mw.change_design()

    def change_pieces_2(self):
        with open('theme.txt', 'r', encoding='utf-8', ) as f:
            data = f.read()
        board = data.split()[-1]
        with open('theme.txt', 'w', encoding='utf-8', ) as f:
            f.write('riohacha ' + board)
        mw.change_design()

    def reference_show(self):
        self.hide()
        ss.show()

    def back(self):
        self.hide()
        fw.show()


class ChooseBoardDesign(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('choose board design.ui', self)
        self.pushButton.clicked.connect(self.change_pieces_1)
        self.pushButton_2.clicked.connect(self.change_pieces_2)
        self.get_back.clicked.connect(self.back)
        self.setFixedSize(self.width(), self.height())
        self.label.setPixmap(QPixmap('ChessImage/cburnett/marble.jpg'))
        self.label_2.setPixmap(QPixmap('ChessImage/riohacha/marble.jpg'))

    def change_pieces_1(self):
        with open('theme.txt', 'r', encoding='utf-8', ) as f:
            data = f.read()
        piece = data.split()[0]
        with open('theme.txt', 'w', encoding='utf-8', ) as f:
            f.write(piece + ' cburnett')
        mw.change_design()

    def change_pieces_2(self):
        with open('theme.txt', 'r', encoding='utf-8', ) as f:
            data = f.read()
        piece = data.split()[0]
        with open('theme.txt', 'w', encoding='utf-8', ) as f:
            f.write(piece + ' riohacha')
        mw.change_design()

    def reference_show(self):
        self.hide()
        ss.show()

    def back(self):
        self.hide()
        fw.show()


class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('first window.ui', self)
        self.playWithFriend.clicked.connect(self.play_with_friend_def)
        self.playWithBot.clicked.connect(self.play_with_bot_def)
        self.settings.clicked.connect(self.settings_def)
        self.setFixedSize(self.width(), self.height())

    def play_with_friend_def(self):
        self.hide()
        sw.show()

    def play_with_bot_def(self):
        self.hide()
        swvb.show()

    def settings_def(self):
        self.hide()
        ss.show()


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.pieses.clicked.connect(self.change_pieces)
        self.board.clicked.connect(self.change_board)
        self.reference.clicked.connect(self.reference_show)
        self.get_back.clicked.connect(self.back)
        self.setFixedSize(self.width(), self.height())

    def change_pieces(self):
        self.hide()
        pd.show()

    def change_board(self):
        self.hide()
        bd.show()

    def reference_show(self):
        r.show()

    def back(self):
        self.hide()
        fw.show()


class Reference(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

    def run(self, color, level_bot=0, flag=False):
        try:
            if not self.login.text() and not self.password.text():
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
                        mw.start_and_get_info(color, self.login.text(), flag, level_bot)
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
                mw.start_and_get_info(color, self.login.text(), flag, level_bot)
                mw.show()
        except Exception as e:
            print(e)


class SecondWindowVsBot(SecondWindow):
    def initUI(self):
        uic.loadUi('second window vs bot.ui', self)
        self.setFixedSize(self.width(), self.height())
        self.level_bot.valueChanged.connect(self.change_level)
        self.status_bar = QStatusBar(self)
        self.status_bar.setGeometry(0, self.height() - 25, self.width(), 25)
        self.setFixedSize(self.width(), self.height())
        self.pushButton.clicked.connect(self.run)

    def change_level(self):
        self.level.setText(str(self.level_bot.value()))

    def run(self, color, level_bot=0, flag=True):
        super().run(color, self.level_bot.value(), flag)


class Checkmate(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('Checkmate.ui', self)
        self.get_back.clicked.connect(self.run)

    def run(self):
        mw.hide()
        cm.hide()
        fw.show()


class Stalemate(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('stalemate.ui', self)
        self.get_back.clicked.connect(self.run)

    def run(self):
        mw.hide()
        sm.hide()
        fw.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fw = FirstWindow()  # First window
    sw = SecondWindow()  # Second window
    mw = Main()  # Main window
    r = Reference()  # Reference
    cm = Checkmate()  # Checkmate
    sm = Stalemate()  # Stalemate
    swvb = SecondWindowVsBot()  # SecondWindowVsBot
    ss = Settings()  # Settings
    pd = ChoosePiecesDesign()  # Pieces design
    bd = ChooseBoardDesign()  # Board design
    fw.show()
    sys.exit(app.exec_())
