
def slide_it(window, value):
    decimal_value = value / 10.0
    window.tempResTxt.setText(f"{decimal_value:.1f}")

def generationToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()

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

def v_genToggle(self):
    # Скрываем два виджета и показываем один
    self.input_dialog.hide()
    self.v_input_dialog.hide()
    self.e_input_dialog.show()



