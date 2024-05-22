from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from ui_loader import load_ui
from event_handlers import toggle_icon_and_move, slide_it, clear_fields

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Загрузка UI
        self.form = load_ui(self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Найти виджет InputDialog
        self.input_dialog = self.findChild(QWidget, 'InputDialog')
        self.input_dialog.hide()
        self.line_4 = self.findChild(QFrame, 'line_4')

        # Найти кнопку и установить начальную иконку
        self.droparrow_button = self.findChild(QPushButton, 'droparrowBtn')
        self.is_down = True
        self.droparrow_button.clicked.connect(lambda: toggle_icon_and_move(self))

        # Создаем QSlider
        self.slider = self.findChild(QSlider, 'slider')
        self.tempResTxt = self.findChild(QLabel, 'tempResTxt')

        # Настройка QSlider
        self.slider.setRange(0, 10)
        self.slider.setSingleStep(1)
        self.slider.setValue(7)

        # Обновляем QLabel с текущим значением слайдера в виде десятичного числа
        initial_value = self.slider.value() / 10.0
        self.tempResTxt.setText(f"{initial_value:.1f}")
        self.slider.valueChanged.connect(lambda value: slide_it(self, value))

        #Найти кнопки генерации текста и очищение полей
        self.genBtn = self.findChild(QPushButton, 'generationBtn')
        self.clearBtn = self.findChild(QPushButton, 'clearBtn')

        #Найти поля ввода данных
        self.headlineEdit = self.findChild(QLineEdit, 'headlineEdit')
        self.audienceEdit = self.findChild(QLineEdit, 'audienceEdit')
        self.keyEdit = self.findChild(QLineEdit, 'keyEdit')
        self.actionEdit = self.findChild(QLineEdit, 'actionEdit')
        self.lengthEdit = self.findChild(QLineEdit, 'lengthEdit')

        # Подключить кнопку очистки к слоту
        self.clearBtn.clicked.connect(lambda: clear_fields(self))

        # Настройка кнопок управления окном
        self.setup_button('close', self.close_window)
        self.setup_button('collapse', self.minimize_window)

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
