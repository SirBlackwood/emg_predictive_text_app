from PyQt6.QtWidgets import QApplication
from app import MainWindow


app = QApplication([])
window = MainWindow()
window.show()
app.exec()

