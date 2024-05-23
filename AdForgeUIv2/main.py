from PyQt5.QtWidgets import QApplication
from main_window import MyWindow

def main():
    app = QApplication([])
    my_window = MyWindow()
    my_window.show()
    app.exec()

if __name__ == '__main__':
    main()
