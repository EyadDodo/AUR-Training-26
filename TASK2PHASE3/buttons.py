from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class Buttons(QWidget):
    start = Signal()
    pause = Signal()
    reset = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._timer_paused = True

        self.start_button = QPushButton("Start")
        self.reset_button = QPushButton("Reset")

        self.start_button.clicked.connect(self._b1_clicked)
        self.reset_button.clicked.connect(self._b2_clicked)

        layout = QHBoxLayout(self)
        layout.addWidget(self.start_button)
        layout.addWidget(self.reset_button)

    @property
    def timer_paused(self) -> bool:
        return self._timer_paused

    @timer_paused.setter
    def timer_paused(self, state: bool) -> None:
        self._timer_paused = state

    def _b1_clicked(self) -> None:
        if self._timer_paused:
            self.start.emit()
        else:
            self.pause.emit()

    def _b2_clicked(self) -> None:
        self.reset.emit()

    def set_running(self) -> None:
        self._timer_paused = False
        self.start_button.setText("Pause")

    def set_paused(self) -> None:
        self._timer_paused = True
        self.start_button.setText("Start")

    def set_initial(self) -> None:
        self._timer_paused = False
        self.start_button.setText("Start")
