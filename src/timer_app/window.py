from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .buttons import Buttons
from .stack import Stack


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Countdown Timer")
        self.setMinimumSize(420, 220)

        central = QWidget()
        layout = QVBoxLayout(central)

        self.stack = Stack()
        self.buttons = Buttons()

        layout.addWidget(self.stack)
        layout.addWidget(self.buttons)

        self.setCentralWidget(central)

        self.buttons.start.connect(self._start_or_resume)
        self.buttons.pause.connect(self._pause)
        self.buttons.reset.connect(self._reset)
        self.stack.time_stopped.connect(self._switch_buttons)

    def _start_or_resume(self) -> None:
        if self.stack.is_running():
            return

        # On the initial input screen, validate and start.
        # On the timer screen, resume after a pause.
        if self.stack.currentWidget() is self.stack.input_page:
            if self.stack.start_counter():
                self.buttons.set_running()
        else:
            self.stack.timer.start()
            self.buttons.set_running()

    def _pause(self) -> None:
        if self.stack.currentWidget() is self.stack.timer_page:
            self.stack.pause()
            self.buttons.set_paused()

    def _reset(self) -> None:
        self.stack.reset()
        self.buttons.set_initial()

    def _switch_buttons(self, finished: bool) -> None:
        if finished and self.stack.remaining_seconds == 0:
            self.buttons.set_initial()
        elif not finished:
            self.buttons.set_running()
