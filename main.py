from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt, QEvent

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Ожидание нажатия левой кнопки мыши')

        # Инициализируем флаг для отслеживания нажатия левой кнопки мыши
        self.left_click_detected = False

        # Добавляем фильтр событий
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # Обработка события нажатия левой кнопки мыши
            self.left_click_detected = True
            return True  # Событие обработано

        return super().eventFilter(obj, event)

    def wait_for_left_click(self):
        # Создаем цикл, ожидающий нажатия левой кнопки мыши
        while not self.left_click_detected:
            QApplication.processEvents()

        # После того, как нажатие было обнаружено, выводим сообщение
        QMessageBox.information(self, 'Информация', 'Левая кнопка мыши была нажата!')

        # Сбросим флаг для следующего использования
        self.left_click_detected = False

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()

    # Ожидаем нажатия левой кнопки мыши
    widget.wait_for_left_click()

    app.exec_()
