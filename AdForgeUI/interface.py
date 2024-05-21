from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # Загрузка UI
        Form, Window = uic.loadUiType("UI/1.ui")

        # Создание экземпляра окна
        self.window = self  # Используем self в качестве главного окна
        self.form = Form()
        self.form.setupUi(self.window)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Найдите QComboBox по его имени
        self.comboBox = self.findChild(QComboBox, 'styleBox')  # Замените 'comboBox' на имя вашего QComboBox

        # Найти кнопку и установить начальную иконку
        self.droparrow_button = self.findChild(QPushButton, 'droparrowBtn')
        if self.droparrow_button:
            self.is_down = True  # начальное состояние иконки
            self.droparrow_button.setIcon(QIcon('images/up-arrow.png'))
            self.droparrow_button.clicked.connect(self.toggle_icon_and_move)

        # Создаем QSlider
        self.slider = self.findChild(QSlider, 'slider')
        self.tempResTxt = self.findChild(QLabel, 'tempResTxt')

        # Настройка QSlider
        self.slider.setRange(0, 10)  # Устанавливаем диапазон от 0 до 10
        self.slider.setSingleStep(1)  # Устанавливаем шаг слайдера
        self.slider.valueChanged.connect(self.slide_it)

        # Найти виджет InputDialog
        self.input_dialog = self.findChild(QWidget, 'InputDialog')
        self.line_4 = self.findChild(QFrame, 'line_4')

        # Настройка кнопок управления окном
        self.setup_button('close', self.close_window)
        self.setup_button('collapse', self.minimize_window)

        self.show()

    def slide_it(self, value):
        # Преобразуем значение слайдера в шаги по 0.1
        decimal_value = value / 10.0
        self.tempResTxt.setText(f"{decimal_value:.1f}")


    def toggle_icon_and_move(self):
        # Переключение иконки
        if self.is_down:
            self.droparrow_button.setIcon(QIcon('images/down-arrow.png'))
        else:
            self.droparrow_button.setIcon(QIcon('images/up-arrow.png'))
        self.is_down = not self.is_down  # переключаем состояние

        # # Перемещение кнопки и диалогового окна
        # current_pos_button = self.droparrow_button.pos()
        # current_pos_dialog = self.input_dialog.pos() if self.input_dialog else QPoint(0, 0)
        # current_pos_line = self.line_4.pos() if self.line_4 else QPoint(0, 0)
        #
        # # if current_pos_button == QPoint(230, 490) and current_pos_dialog == QPoint(210, 580) and current_pos_line == QPoint(0, 487):
        # #     self.droparrow_button.move(230, 150)
        # #     if self.input_dialog:
        # #         self.input_dialog.move(210, 240)
        # #         self.line_4.move(0, 150)
        # # else:
        # #     self.droparrow_button.move(230, 490)
        # #     if self.input_dialog:
        # #         self.input_dialog.move(210, 580)
        # #         self.line_4.move(0, 487)


    def setup_button(self, button_name, callback):
        button = self.findChild(QPushButton, button_name)
        if button is not None:
            button.clicked.connect(callback)
        else:
            print(f"Button '{button_name}' not found. Check the object name in your .ui file.")

    def close_window(self):
        self.close()

    def minimize_window(self):
        self.showMinimized()

def main():
    app = QApplication([])
    my_window = MyWindow()
    app.exec()

if __name__ == '__main__':
    main()
