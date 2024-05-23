from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint

from ui_loader import load_ui
from event_handlers import newGenToggle, uparrowToggle, downarrowToggle, slide_it, generationToggle, v_generationToggle, edit_ad
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QStyle
import os
import json


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

        # Инициализация кнопки для удаления истории объявлений
        self.delete_btn = self.findChild(QPushButton, 'deleteGenBtn')
        self.delete_btn.clicked.connect(self.delete_ad_data)



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

        # Кнопки сохранения и копирования
        self.save_btn = self.findChild(QPushButton, 'saveBtn')
        self.save_btn.clicked.connect(self.save_ad_text)

        self.copy_btn = self.findChild(QPushButton, 'copyBtn')
        self.copy_btn.clicked.connect(self.copy_ad_text)

        # Переключения страниц
        self.generation = self.findChild(QPushButton, 'generationBtn')
        self.generation.clicked.connect(lambda: generationToggle(self))

        self.v_eneration = self.findChild(QPushButton, 'v_generationBtn')
        self.v_eneration.clicked.connect(lambda: v_generationToggle(self))

        self.droparrow_button = self.findChild(QPushButton, 'downarrowBtn')
        self.droparrow_button.clicked.connect(lambda: downarrowToggle(self))

        self.uparrow_button = self.findChild(QPushButton, 'uparrowBtn')
        self.uparrow_button.clicked.connect(lambda: uparrowToggle(self))

        self.newGeneration = self.findChild(QPushButton, 'newGenerationBtn')
        self.newGeneration.clicked.connect(lambda: newGenToggle(self))

        # Добавление кнопки для редактирования и полей для редактирования
        self.e_generation = self.findChild(QPushButton, 'e_generationBtn')
        self.e_generation.clicked.connect(lambda: edit_ad(self))

        self.e_model = self.findChild(QComboBox, 'e_modelBox')
        self.e_potok = self.findChild(QComboBox, 'e_potokBox')
        self.e_slider = self.findChild(QSlider, 'e_slider')
        self.e_change = self.findChild(QLineEdit, 'e_changeEdit')

        # # Добавление новых элементов для отображения объявлений
        # self.ad_list_widget = self.findChild(QListWidget, 'adListWidget')
        # self.view_ad_button = self.findChild(QPushButton, 'viewAdButton')
        # self.delete_ad_button = self.findChild(QPushButton, 'deleteAdButton')
        # self.prev_ad_button = self.findChild(QPushButton, 'prevAdButton')
        # self.next_ad_button = self.findChild(QPushButton, 'nextAdButton')

        # Добавление новых элементов для отображения объявлений
        self.ad_list_widget = self.findChild(QListWidget, 'adListWidget')
        self.view_ad_button = self.findChild(QPushButton, 'viewAdButton')
        self.delete_ad_button = self.findChild(QPushButton, 'deleteAdButton')
        self.refresh_ad_button = self.findChild(QPushButton, 'refreshAdButton')  # заменить кнопку на refreshAdButton

        self.view_ad_button.clicked.connect(self.view_ad)
        self.delete_ad_button.clicked.connect(self.delete_ad)
        # self.prev_ad_button.clicked.connect(self.prev_ad)
        # self.next_ad_button.clicked.connect(self.next_ad)
        self.refresh_ad_button.clicked.connect(self.refresh_ad_list)  # подключить сигнал к функции обновления

        # Загрузка и отображение объявлений
        self.ads = self.load_ads_from_json()
        self.current_ad_index = 0
        self.update_ad_display()
        self.update_ad_list_widget()

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

    def save_ad_text(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "объявление.txt",
                                                   "Text Files (*.txt);;Word Documents (*.docx);;PDF Files (*.pdf);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.answer.toPlainText())

    def copy_ad_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.answer.toPlainText())
        QMessageBox.information(self, "Копирование", "Текст успешно скопирован!")


    def delete_ad_data(self):
        try:
            os.remove('ad_data.json')
            QMessageBox.information(self, "Удаление", "Файл истории объявлений успешно удален!")
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл истории объявлений не найден!")

    def load_ads_from_json(self):
        try:
            with open('ad_data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def update_ad_display(self):
        if self.ads:
            ad = self.ads[self.current_ad_index]
            self.result.setText(f"Заголовок: {ad['headline']}\nДата последнего редактирования: {ad['creation_date']}")
        else:
            self.result.setText("Нет доступных объявлений.")

    def update_ad_display(self):
        if self.ads:
            ad = self.ads[self.current_ad_index]
            self.result.setText(f"Заголовок: {ad['headline']}\nДата последнего редактирования: {ad['creation_date']}")
            self.answer.setText(ad['ad_text'])  # добавлено для отображения текста объявления в answerText
        else:
            self.result.setText("Нет доступных объявлений.")
            self.answer.clear()  # очистка текстового поля, если нет доступных объявлений

    def view_ad(self):
        current_item = self.ad_list_widget.currentItem()
        if current_item:
            index = self.ad_list_widget.row(current_item)
            self.current_ad_index = index
            self.update_ad_display()
            # Переход в режим редактирования
            self.input_dialog.hide()
            self.v_input_dialog.hide()
            self.e_input_dialog.show()
            self.result.show()
            self.answer.show()
            # Заполнение полей в режиме редактирования
            ad = self.ads[self.current_ad_index]
            self.e_change.setText(ad['headline'])
            # Дополнительно: можно заполнить другие поля в режиме редактирования, если необходимо

    def refresh_ad_list(self):
        self.ads = self.load_ads_from_json()
        self.update_ad_list_widget()
        self.update_ad_display()

    def update_ad_list_widget(self):
        self.ad_list_widget.clear()
        for ad in self.ads:
            self.ad_list_widget.addItem(f"{ad['headline']} - {ad['creation_date']}")

    def delete_ad(self):
        current_item = self.ad_list_widget.currentItem()
        if current_item:
            index = self.ad_list_widget.row(current_item)
            del self.ads[index]
            self.update_ad_list_widget()
            self.save_ads_to_json()
            if self.ads:
                self.current_ad_index = 0
            self.update_ad_display()

    def prev_ad(self):
        if self.current_ad_index > 0:
            self.current_ad_index -= 1
            self.update_ad_display()

    def next_ad(self):
        if self.current_ad_index < len(self.ads) - 1:
            self.current_ad_index += 1
            self.update_ad_display()

    def save_ads_to_json(self):
        with open('ad_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.ads, file, ensure_ascii=False, indent=4)

