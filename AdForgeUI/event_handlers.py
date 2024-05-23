import asyncio
from ProjectDirectory.AdForgePackageVer3.ad_manager import AdManager
from ProjectDirectory.AdForgePackageVer3.ad_editor import AdEditor
from ProjectDirectory.AdForgePackageVer3.config import proxies

def slide_it(window, value):
    decimal_value = value / 10.0
    window.tempResTxt.setText(f"{decimal_value:.1f}")

def generationToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()
    self.result.show()
    self.answer.show()

    try:
        # Получаем текст из всех QLineEdit
        texts = [
            self.headline.text(),
            self.audience.text(),
            self.action.text(),
            self.length.text(),
            self.key.text(),
            self.style.currentText(),
            self.model.currentText(),
            self.potok.currentText()
        ]

        # Объединяем текст с разделителем (например, новой строкой)
        combined_text = '\n'.join(texts)

        # Устанавливаем объединенный текст в QLabel
        self.result.setText(combined_text)
    except Exception as e:
        print(f"Error: {e}")


def downarrowToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.show()
    self.v_input_dialog.hide()
    self.e_input_dialog.hide()

def uparrowToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.hide()
    self.v_input_dialog.show()
    self.e_input_dialog.hide()

def newGenToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.hide()
    self.v_input_dialog.show()
    self.e_input_dialog.hide()
    self.result.hide()
    self.answer.hide()


def v_genToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()
    self.result.show()
    self.answer.show()

    try:
        # Получаем текст из всех QLineEdit
        texts = [
            self.v_headline.text(),
            self.v_audience.text(),
        ]

        # Объединяем текст с разделителем (например, новой строкой)
        combined_text = '\n'.join(texts)

        # Устанавливаем объединенный текст в QLabel
        self.result.setText(combined_text)
    except Exception as e:
        print(f"Error: {e}")