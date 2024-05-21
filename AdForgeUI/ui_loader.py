from PyQt5 import uic

def load_ui(window):
    Form, Window = uic.loadUiType("UI/1.ui")
    form = Form()
    form.setupUi(window)
    return form
