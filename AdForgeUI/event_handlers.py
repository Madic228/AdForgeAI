from PyQt5.QtGui import QIcon

def toggle_icon_and_move(window):
    if window.is_down:
        window.droparrow_button.setIcon(QIcon('images/down-arrow.png'))
    else:
        window.droparrow_button.setIcon(QIcon('images/up-arrow.png'))
    window.is_down = not window.is_down

    # Можно добавить логику для перемещения кнопки и диалогового окна

    # def toggle_icon_and_move(self):
    #     # Переключение иконки
    #     if self.is_down:
    #         self.droparrow_button.setIcon(QIcon('images/down-arrow.png'))
    #     else:
    #         self.droparrow_button.setIcon(QIcon('images/up-arrow.png'))
    #     self.is_down = not self.is_down  # переключаем состояние

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


def slide_it(window, value):
    decimal_value = value / 10.0
    window.tempResTxt.setText(f"{decimal_value:.1f}")
