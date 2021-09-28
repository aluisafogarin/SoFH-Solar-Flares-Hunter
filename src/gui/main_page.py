import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon("icons/sun_icon.png"))
        self.setWindowTitle("Software TCC")
        self.resize(1000, 650)


root = QApplication(sys.argv)
app = Window()
app.show()
sys.exit(root.exec_())
