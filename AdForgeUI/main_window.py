import sys
import asyncio
import logging
from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QSlider, QLabel, QLineEdit, QComboBox, \
    QTextBrowser, QPushButton, QTextEdit

from ui_loader import load_ui
from event_handlers import v_genToggle, newGenToggle, uparrowToggle, downarrowToggle, slide_it, generationToggle
from ProjectDirectory.AdForgePackageVer4.ad_manager import AdManager
from ProjectDirectory.AdForgePackageVer4.config import proxies


def create_logger(path, widget: QTextEdit):
    log = logging.getLogger('main')
    log.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        ('#%(levelname)-s, %(pathname)s, line %(lineno)d, [%(asctime)s]: '
         '%(message)s'), datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(('#%(levelname)-s, %(pathname)s, '
                                           'line %(lineno)d: %(message)s'))

    log_window_formatter = logging.Formatter(
        '#%(levelname)-s, %(message)s\n'
    )

    file_handler = logging.FileHandler(path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)

    log_window_handler = logging.Handler()
    log_window_handler.emit = lambda record: widget.insertPlainText(
        log_window_handler.format(record)
    )
    log_window_handler.setLevel(logging.DEBUG)
    log_window_handler.setFormatter(log_window_formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)
    log.addHandler(log_window_handler)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Логирование в текстовое поле
        self.log_widget = QTextEdit(self)
        self.log_widget.setReadOnly(True)
        self.log_widget.setGeometry(10, 10, 600, 100)  # Adjust the size and position as needed
        self.log_widget.setWindowTitle('Logs')
        self.log_widget.show()
        create_logger('app.log', self.log_widget)
        self.logger = logging.getLogger('main')
        self.logger.info("Приложение инициализировано")

        self.initUI()
        self.ad_manager = AdManager(proxies=proxies)  # Инициализация AdManager
        self.logger.info("AdManager инициализирован")

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

        # Настройка кнопок управления окном
        self.setup_button('close', self.close_window)
        self.setup_button('collapse', self.minimize_window)

        # TextFields
        self.v_headline = self.findChild(QLineEdit, 'v_headlineEdit')
        self.v_audience = self.findChild(QLineEdit, 'v_audienceEdit')

        self.headline = self.findChild(QLineEdit, 'headlineEdit')
        self.audience = self.findChild(QLineEdit, 'audienceEdit')
        self.action = self.findChild(QLineEdit, 'actionEdit')
        self.length = self.findChild(QLineEdit, 'lengthEdit')
        self.key = self.findChild(QLineEdit, 'keyEdit')

        self.style = self.findChild(QComboBox, 'styleBox')
        self.model = self.findChild(QComboBox, 'modelBox')
        self.potok = self.findChild(QComboBox, 'potokBox')

        self.result = self.findChild(QTextBrowser, 'resultText')
        self.result.hide()

        self.answer = self.findChild(QTextBrowser, 'answerText')
        self.answer.hide()

        # Переключения страниц
        # Переключения страниц
        self.generation = self.findChild(QPushButton, 'generationBtn')
        self.generation.clicked.connect(lambda: asyncio.create_task(generationToggle(self)))  # Изменение здесь!

        self.v_eneration = self.findChild(QPushButton, 'v_generationBtn')
        self.v_eneration.clicked.connect(lambda: v_genToggle(self))

        self.droparrow_button = self.findChild(QPushButton, 'downarrowBtn')
        self.droparrow_button.clicked.connect(lambda: downarrowToggle(self))

        self.uparrow_button = self.findChild(QPushButton, 'uparrowBtn')
        self.uparrow_button.clicked.connect(lambda: uparrowToggle(self))

        self.newGeneration = self.findChild(QPushButton, 'newGenerationBtn')
        self.newGeneration.clicked.connect(lambda: newGenToggle(self))

        # Инициализация для перетаскивания окна
        self.oldPos = self.pos()

        self.logger.info("UI инициализирован")

    async def run_generation_toggle(self):
        await generationToggle(self)

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
            self.logger.info(f"Кнопка '{button_name}' привязана к функции {callback.__name__}")
        else:
            self.logger.error(f"Кнопка '{button_name}' не найдена. Проверьте имя объекта в .ui файле")

    def close_window(self):
        self.logger.info("Закрытие окна")
        self.close()

    def minimize_window(self):
        self.logger.info("Сворачивание окна")
        self.showMinimized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MyWindow()
    window.show()
    with loop:
        loop.run_forever()
