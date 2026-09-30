from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .stack import Stack


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Digital Watch")
        self.setMinimumSize(420, 220)

        central = QWidget()
        layout = QVBoxLayout(central)

        self.stack = Stack()

        layout.addWidget(self.stack)

        self.setCentralWidget(central)