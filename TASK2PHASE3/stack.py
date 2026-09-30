from PySide6.QtWidgets import QStackedWidget, QLabel, QWidget
from PySide6.QtCore import QTimer, Qt, QTime


class Stack(QStackedWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignCenter)
        self.clock.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
            }
        """)

        self.addWidget(self.clock)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.update_clock()

    def update_clock(self) -> None:
        self.clock.setText(QTime.currentTime().toString("HH:mm:ss"))