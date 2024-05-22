from PyQt5.QtCore import QPoint
from PyQt5.QtGui import *

def toggle_icon_and_move(window):
    if window.is_down:
        window.droparrow_button.setIcon(QIcon('images/up-arrow.png'))
    else:
        window.droparrow_button.setIcon(QIcon('images/down-arrow.png'))
    window.is_down = not window.is_down

    # Перемещение кнопки и диалогового окна
    current_pos_button = window.droparrow_button.pos()
    current_pos_dialog = window.input_dialog.pos() if window.input_dialog else QPoint(0, 0)
    current_pos_line = window.line_4.pos() if window.line_4 else QPoint(0, 0)

    if current_pos_button == QPoint(230, 490) and current_pos_dialog == QPoint(10, 509) and current_pos_line == QPoint(0, 487):
        window.droparrow_button.move(230, 150)
        if window.input_dialog:
            window.input_dialog.move(10, 180)
            window.line_4.move(0, 150)
    else:
        window.droparrow_button.move(230, 490)
        if window.input_dialog:
            window.input_dialog.move(10, 509)
            window.line_4.move(0, 487)


def slide_it(window, value):
    decimal_value = value / 10.0
    window.tempResTxt.setText(f"{decimal_value:.1f}")

def clear_fields(self):
    # Очистить все QLineEdit
    self.headlineEdit.clear()
    self.audienceEdit.clear()
    self.keyEdit.clear()
    self.actionEdit.clear()
    self.lengthEdit.clear()