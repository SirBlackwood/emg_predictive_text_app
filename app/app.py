from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import Qt
from PyQt6 import uic
from twolettersdict import two_letters_dict
from serverthread import ServerThread
from textpridiction import predict_text
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Нахождение кнопок по их именам
        self.button3 = self.findChild(QPushButton, "button3")
        self.button2 = self.findChild(QPushButton, "button2")
        self.button1 = self.findChild(QPushButton, "button1")
        self.cancel_button = self.findChild(QPushButton, "cancel_button")
        self.matches = None
        self.is_first_word = True

        # Нахождение QLineEdit по его имени
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.server_thread = ServerThread()
        self.server_thread.data_received.connect(self.update_ui)  # Подключение сигнала к слоту
        self.server_thread.start()

        # Загрузка дизайна из файла .ui
        self.load_ui()

        # Сохранение исходных имен кнопок
        self.initial_names = {
            "button1": self.button1.text(),
            "button2": self.button2.text(),
            "button3": self.button3.text()
        }

        self.button1.clicked.connect(lambda: self.check_and_append(self.button1))
        self.button2.clicked.connect(lambda: self.check_and_append(self.button2))
        self.button3.clicked.connect(lambda: self.check_and_append(self.button3))
        self.cancel_button.clicked.connect(lambda: self.cancel())
        self.buttons = {"3": self.button1, "1": self.button2, "2": self.button3}

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_1:
            self.check_and_append(self.button1)
        elif event.key() == Qt.Key.Key_2:
            self.check_and_append(self.button2)
        elif event.key() == Qt.Key.Key_3:
            self.check_and_append(self.button3)
        elif event.key() == Qt.Key.Key_Backspace:
            self.cancel()

    def update_ui(self, data):
        if data == '0':
            self.cancel()
            return
        self.check_and_append(self.buttons[data])

    def load_ui(self):
        ui_file = "design.ui"
        uic.loadUi(ui_file, self)

    def cancel(self):
        pattern = r'\s\w{2}$'
        match = re.search(pattern, self.lineEdit.text())

        if match or len(self.lineEdit.text()) == 2:
            self.lineEdit.setText(self.lineEdit.text()[:-2])

        self.button1.setText(self.initial_names["button1"])
        self.button2.setText(self.initial_names["button2"])
        self.button3.setText(self.initial_names["button3"])

    def check_and_append(self, clicked_button):
        clicked_button_name = clicked_button.objectName()
        current_names = {
            "button1": self.button1.text(),
            "button2": self.button2.text(),
            "button3": self.button3.text()
        }

        name_lines = current_names[clicked_button_name].split('\n')

        if clicked_button.text().strip() == clicked_button.text() and '\n' not in clicked_button.text():
            current_text = self.lineEdit.text()
            split_current_text = current_text.split('  ')
            if len(split_current_text[-1]) == 2:
                self.lineEdit.setText(self.lineEdit.text()[:-2] + clicked_button.text() + '  ')
            else:
                self.lineEdit.setText(current_text + clicked_button.text())
            line_edit_text = self.lineEdit.text()
            split_edit_text = line_edit_text.split('  ')
            if len(split_edit_text[-1]) == 2:
                if self.is_first_word:
                    self.is_first_word = False
                    self.matches = predict_text(split_edit_text[-1])
                    print(split_edit_text[-1])
                else:
                    print('rofl')
                    context = ' '.join(map(str, split_edit_text[:len(split_edit_text) - 1]))
                    print(context)
                    self.matches = predict_text(split_edit_text[-1], context, len(split_edit_text) - 1)
                self.button1.setText('\n'.join(self.matches[:3]).upper())
                self.button2.setText('\n'.join(self.matches[3:6]).upper())
                self.button3.setText('\n'.join(self.matches[6:]).upper())
            else:
                self.button1.setText(self.initial_names["button1"])
                self.button2.setText(self.initial_names["button2"])
                self.button3.setText(self.initial_names["button3"])

        if len(name_lines) >= 3:
            new_name1 = name_lines[0].replace("  ", "\n", 2)
            new_name2 = name_lines[1].replace("  ", "\n", 2)
            new_name3 = name_lines[2].replace("  ", "\n", 2)
            self.button1.setText(new_name1)
            self.button2.setText(new_name2)
            self.button3.setText(new_name3)

        if len(name_lines) == 2:
            self.button1.setText(name_lines[0])
            self.button2.setText(name_lines[1])
            self.button3.setText("")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
