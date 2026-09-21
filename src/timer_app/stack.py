from PySide6.QtCore import QIntValidator, QTimer, Signal, Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QStackedWidget, QWidget


class Stack(QStackedWidget):
    time_stopped = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.input_page = QWidget()
        self.timer_page = QWidget()

        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Enter time in seconds")
        self.time_input.setValidator(QIntValidator(1, 359999, self.time_input))
        self.time_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timer_label = QLabel("00:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        from PySide6.QtWidgets import QVBoxLayout

        input_layout = QVBoxLayout(self.input_page)
        input_layout.addWidget(self.time_input)

        timer_layout = QVBoxLayout(self.timer_page)
        timer_layout.addWidget(self.timer_label)

        self.addWidget(self.input_page)
        self.addWidget(self.timer_page)
        self.setCurrentWidget(self.input_page)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._decrement)

        self.remaining_seconds = 0

    def start_counter(self) -> bool:
        text = self.time_input.text().strip()

        if not text:
            return False

        seconds = int(text)
        if seconds <= 0:
            return False

        if self.remaining_seconds == 0:
            self.remaining_seconds = seconds

        self._update_label()
        self.setCurrentWidget(self.timer_page)
        self.timer.start()
        self.time_stopped.emit(False)
        return True

    def _decrement(self) -> None:
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self._update_label()

        if self.remaining_seconds == 0:
            self.timer.stop()
            self.time_stopped.emit(True)

    def _update_label(self) -> None:
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def reset(self) -> None:
        self.timer.stop()
        self.remaining_seconds = 0
        self.timer_label.setText("00:00")
        self.time_input.clear()
        self.setCurrentWidget(self.input_page)
        self.time_stopped.emit(True)

    def pause(self) -> None:
        self.timer.stop()
        self.time_stopped.emit(True)

    def is_running(self) -> bool:
        return self.timer.isActive()
