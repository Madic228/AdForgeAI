import logging
import requests
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication

logger = logging.getLogger('main')

def slide_it(self, value):
    decimal_value = value / 10.0
    self.tempResTxt.setText(f"{decimal_value:.1f}")
    self.e_tempResTxt.setText(f"{decimal_value:.1f}")
    logger.info(f"Слайдер перемещен на значение: {decimal_value:.1f}")


def generationToggle(self):
    logger.info("Кнопка 'Генерировать объявление' нажата")

    # Получаем значения полей
    headline = self.headline.text()
    audience = self.audience.text()
    key = self.key.text()
    call_to_action = self.action.text()
    style = self.style.currentText()
    length_limit = self.length.text()
    model_choice = self.model.currentIndex() + 1  # Индексы начинаются с 0
    temperature = self.slider.value() / 10.0
    stream = self.potok.currentText() == "Включить обработку"

    # Проверяем, что поля headline и audience заполнены
    if not headline or not audience:
        logger.warning("Поля 'Заголовок' и 'Целевая аудитория' должны быть заполнены")
        QMessageBox.warning(self, "Ошибка", "Поля 'Заголовок' и 'Целевая аудитория' должны быть заполнены")
        return

    # Если поле key не пустое, проверяем, что key можно преобразовать в целое число
    if length_limit:
        try:
            length_int = int(length_limit)
        except ValueError:
            logger.warning("Поле 'Длина' должно быть целым числом")
            QMessageBox.warning(self, "Ошибка", "Поле 'Длина' должно быть целым числом")
            return

    # Скрываем неиспользуемые виджеты и показываем нужные
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()
    self.result.show()
    self.answer.show()

    try:
        # Продолжаем выполнение, если оба поля заполнены и key (если есть) корректный
        # Формируем текст объявления
        combined_text = f"Заголовок: {headline}\nЦелевая аудитория: {audience}\n" \
                        f"Призыв к действию: {call_to_action}\n" \
                        f"Стиль: {style}\nОграничение по длине: {length_limit}\n" \
                        f"Выбранная модель: {model_choice}\nТемпература: {temperature}\n" \
                        f"Потоковая обработка: {'Включена' if stream else 'Отключена'}"

        # Отображаем сформированный текст в окне
        self.result.setText(combined_text)

        # Подготовка данных для отправки
        payload = {
            "headline": headline,
            "audience": audience,
            "call_to_action": call_to_action,
            "style": style,
            "model_choice": model_choice,
            "temperature": temperature,
            "stream": stream
        }

        # Добавляем key_benefits только если поле key не пустое
        if key:
            payload["key_benefits"] = key

        # Добавляем length_limit только если оно не пустое
        if length_limit:
            payload["length_limit"] = int(length_limit)

        logger.info("Отправка POST запроса на сервер FastAPI")
        response = requests.post("http://localhost:8000/generate_ad", json=payload)

        # Проверяем статус ответа
        if response.status_code == 200:
            ad_text = response.json().get("ad_text", "")
            self.answer.setText(ad_text)
            logger.info("Объявление успешно сгенерировано и получено от сервера")
        else:
            error_message = response.json().get("detail", "Неизвестная ошибка")
            raise Exception(error_message)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")


def v_generationToggle(self):
    logger.info("Кнопка 'Генерировать объявление' нажата")

    # Получаем значения полей
    v_headline = self.v_headline.text()
    v_audience = self.v_audience.text()
    # Проверяем, что поля headline и audience заполнены
    if not v_headline or not v_audience:
        logger.warning("Поля 'Заголовок' и 'Целевая аудитория' должны быть заполнены")
        QMessageBox.warning(self, "Ошибка", "Поля 'Заголовок' и 'Целевая аудитория' должны быть заполнены")
        return

    # Скрываем неиспользуемые виджеты и показываем нужные
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()
    self.result.show()
    self.answer.show()

    try:
        # Продолжаем выполнение, если оба поля заполнены
        length_limit = self.length.text()
        model_choice = self.model.currentIndex() + 1  # Индексы начинаются с 0
        temperature = self.slider.value() / 10.0
        stream = self.potok.currentText() == "Включить обработку"

        # Формируем текст объявления
        combined_text = f"Заголовок: {v_headline}\nЦелевая аудитория: {v_audience}\n" \
                        f"Выбранная модель: {model_choice}\nТемпература: {temperature}\n" \
                        f"Потоковая обработка: {'Включена' if stream else 'Отключена'}"

        # Отображаем сформированный текст в окне
        self.result.setText(combined_text)

        # Подготовка данных для отправки
        payload = {
            "headline": v_headline,
            "audience": v_audience,
            "model_choice": model_choice,
            "temperature": temperature,
            "stream": stream
        }
        # Добавляем length_limit только если оно не пустое
        if length_limit:
            payload["length_limit"] = int(length_limit)

        logger.info("Отправка POST запроса на сервер FastAPI")
        response = requests.post("http://localhost:8000/generate_ad", json=payload)

        # Проверяем статус ответа
        if response.status_code == 200:
            ad_text = response.json().get("ad_text", "")
            self.answer.setText(ad_text)
            logger.info("Объявление успешно сгенерировано и получено от сервера")
        else:
            error_message = response.json().get("detail", "Неизвестная ошибка")
            raise Exception(error_message)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")


def edit_ad(self):
    logger.info("Кнопка 'Применить изменения' нажата")

    model_choice = self.e_model.currentIndex() + 1  # Индексы начинаются с 0
    temperature = self.e_slider.value() / 10.0
    stream = self.e_potok.currentText() == "Включить обработку"
    edit_instructions = self.e_change.text()

    # Получение текущего текста объявления
    old_ad_text = self.answer.toPlainText()

    # Создаем словарь с параметрами
    edit_request = {
        "old_ad_text": old_ad_text,
        "edit_instructions": edit_instructions,
        "model_choice": model_choice,
        "temperature": temperature,
        "stream": stream
    }

    try:
        # Отправляем запрос на сервер
        response = requests.post("http://127.0.0.1:8000/edit_ad", json=edit_request)

        if response.status_code == 200:
            new_ad_text = response.json().get("ad_text")
            self.answer.setText(new_ad_text)
            self.result.setText(f"Модель: {model_choice}\nПотоковая обработка: {'Вкл' if stream else 'Выкл'}\nТемпература: {temperature}")
        else:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при редактировании объявления: {response.text}")

    except Exception as e:
        logger.error(f"Ошибка при редактировании объявления: {e}")
        QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")

def downarrowToggle(self):
    self.input_dialog.show()
    self.v_input_dialog.hide()
    self.e_input_dialog.hide()

    # Получаем текст из первого QLineEdit
    text = self.v_headline.text()
    # Устанавливаем текст во второй QLineEdit
    self.headline.setText(text)
    # Получаем текст из первого QLineEdit
    text = self.v_audience.text()
    # Устанавливаем текст во второй QLineEdit
    self.audience.setText(text)

    logger.info("Переход к InputDialog")

def uparrowToggle(self):
    self.input_dialog.hide()
    self.v_input_dialog.show()
    self.e_input_dialog.hide()

    # Получаем текст из первого QLineEdit
    text = self.headline.text()
    # Устанавливаем текст во второй QLineEdit
    self.v_headline.setText(text)
    # Получаем текст из первого QLineEdit
    text = self.audience.text()
    # Устанавливаем текст во второй QLineEdit
    self.v_audience.setText(text)

    logger.info("Переход к VisibleInputDialog")

def newGenToggle(self):
    self.input_dialog.hide()
    self.v_input_dialog.show()
    self.e_input_dialog.hide()
    self.result.hide()
    self.answer.hide()
    logger.info("Переход к новой генерации")

    self.tempResTxt.setText("0.7")
    self.e_tempResTxt.setText("0.7")
    self.slider.setValue(7)
    self.e_slider.setValue(7)

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


def clear(self):
    self.style.setCurrentIndex(0)
    self.model.setCurrentIndex(0)
    self.potok.setCurrentIndex(0)

    self.tempResTxt.setText("0.7")
    self.slider.setValue(7)


