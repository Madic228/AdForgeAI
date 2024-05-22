from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint
from ui_loader import load_ui
from event_handlers import v_genToggle, newGenToggle, uparrowToggle, downarrowToggle, slide_it, generationToggle

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

        # Найти виджет VisibleInputDialog
        self.v_input_dialog = self.findChild(QWidget, 'VisibleInputDialog')
        self.line_6 = self.findChild(QFrame, 'line_6')

        # Найти виджет EditInputDialog
        self.e_input_dialog = self.findChild(QWidget, 'EditInputDialog')
        self.e_input_dialog.hide()
        self.line_7 = self.findChild(QFrame, 'line_7')

        # self.is_down = True
        # self.droparrow_button.clicked.connect(lambda: toggle_icon_and_move(self))

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

        # Переопределение метода mousePressEvent
        self.slider.mousePressEvent = self.create_mouse_press_event(self.slider.mousePressEvent)

        #Найти кнопки генерации текста и очищение полей
        self.genBtn = self.findChild(QPushButton, 'generationBtn')

        # Настройка кнопок управления окном
        self.setup_button('close', self.close_window)
        self.setup_button('collapse', self.minimize_window)

        # Переключения страниц
        self.newGeneration = self.findChild(QPushButton, 'generationBtn')
        self.newGeneration.clicked.connect(lambda: generationToggle(self))

        self.newGeneration = self.findChild(QPushButton, 'v_generationBtn')
        self.newGeneration.clicked.connect(lambda: v_genToggle(self))

        self.droparrow_button = self.findChild(QPushButton, 'downarrowBtn')
        self.droparrow_button.clicked.connect(lambda: downarrowToggle(self))

        self.uparrow_button = self.findChild(QPushButton, 'uparrowBtn')
        self.uparrow_button.clicked.connect(lambda: uparrowToggle(self))

        self.newGeneration = self.findChild(QPushButton, 'newGenerationBtn')
        self.newGeneration.clicked.connect(lambda: newGenToggle(self))


        # Инициализация для перетаскивания окна
        self.oldPos = self.pos()

    def create_mouse_press_event(self, original_mouse_press_event):
        def new_mouse_press_event(event):
            if event.button() == Qt.LeftButton:
                value = QStyle.sliderValueFromPosition(
                    self.slider.minimum(),
                    self.slider.maximum(),
                    event.x(),
                    self.slider.width()
                )
                self.slider.setValue(value)
                event.accept()
            original_mouse_press_event(event)

        return new_mouse_press_event

    def mousePressEvent(self, event, **kwargs):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event, **kwargs):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            if self.oldPos.y() < self.pos().y() + 50:  # Проверка, если клик произошел в верхней части окна
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()


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
