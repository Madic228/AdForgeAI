import asyncio
import logging
import requests
from PyQt5.QtWidgets import QMessageBox

logger = logging.getLogger('main')

def slide_it(window, value):
    decimal_value = value / 10.0
    window.tempResTxt.setText(f"{decimal_value:.1f}")
    logger.info(f"Слайдер перемещен на значение: {decimal_value:.1f}")

def generationToggle(self):
    # Скрываем неиспользуемые виджеты и показываем нужные
    logger.info("Кнопка 'Генерировать объявление' нажата")

    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()
    self.result.show()
    self.answer.show()

    try:
        # Получаем значения полей
        headline = self.headline.text()
        audience = self.audience.text()

        # Продолжаем выполнение, если оба поля заполнены
        key_benefits = self.key.text()
        call_to_action = self.action.text()
        style = self.style.currentText()
        length_limit = self.length.text()
        model_choice = self.model.currentIndex() + 1  # Индексы начинаются с 0
        temperature = self.slider.value() / 10.0
        stream = self.potok.currentText() == "Включить обработку"

        # Формируем текст объявления
        combined_text = f"Заголовок: {headline}\nЦелевая аудитория: {audience}\n" \
                        f"Преимущества: {key_benefits}\nПризыв к действию: {call_to_action}\n" \
                        f"Стиль: {style}\nОграничение по длине: {length_limit}\n" \
                        f"Выбранная модель: {model_choice}\nТемпература: {temperature}\n" \
                        f"Потоковая обработка: {'Включена' if stream else 'Отключена'}"

        # Отображаем сформированный текст в окне
        self.result.setText(combined_text)

        # Отправляем данные на сервер FastAPI
        payload = {
            "headline": headline,
            "audience": audience,
            "key_benefits": key_benefits,
            "call_to_action": call_to_action,
            "style": style,
            "length_limit": int(length_limit) if length_limit else None,
            "model_choice": model_choice,
            "temperature": temperature,
            "stream": stream
        }
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
            logger.info("Объявление успешно отредактировано и получено от сервера")
        else:
            error_message = response.json().get("detail", "Неизвестная ошибка")
            raise Exception(error_message)

    except Exception as e:
        logger.error(f"Ошибка при редактировании объявления: {e}")
        QMessageBox.warning(self, "Ошибка", f"Произошла ошибка: {e}")


def downarrowToggle(self):
    self.input_dialog.show()
    self.v_input_dialog.hide()
    self.e_input_dialog.hide()
    logger.info("Переход к InputDialog")

def uparrowToggle(self):
    self.input_dialog.hide()
    self.v_input_dialog.show()
    self.e_input_dialog.hide()
    logger.info("Переход к VisibleInputDialog")

def newGenToggle(self):
    self.input_dialog.hide()
    self.v_input_dialog.show()
    self.e_input_dialog.hide()
    self.result.hide()
    self.answer.hide()
    logger.info("Переход к новой генерации")

def v_generationToggle(self):
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()
    self.result.show()
    self.answer.show()

    try:
        texts = [
            self.v_headline.text(),
            self.v_audience.text(),
        ]

        combined_text = '\n'.join(texts)
        self.result.setText(combined_text)
        logger.info("Тексты объединены и отображены")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
