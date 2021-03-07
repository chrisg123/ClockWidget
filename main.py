import sys
import signal
import time
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QSize, QTimer, QPointF
from PyQt5.QtGui import QColor

from ClockWidget import ClockWidget

def main():
    signal.signal(signal.SIGINT, sigint)

    app = QApplication(['_'])

    window = QWidget()
    layout = QGridLayout(window)
    layout.setSpacing(0)
    layout.setContentsMargins(0,0,0,0)
    window.setLayout(layout)
    window.setFixedSize(QSize(400, 800))

    clock = ClockWidget(window, window.size(), 0.1)
    now = datetime.datetime.now()
    clock.set_time(now.hour, now.minute, now.second)

    clock.set_background_color(Qt.black)
    clock.set_foreground_color(Qt.white)
    clock.set_hr_hand_color(QColor(0,255,0))
    clock.set_min_hand_color(QColor(255,0,0))
    clock.set_sec_hand_color(Qt.white)

    layout.addWidget(clock,0,0,Qt.AlignCenter)
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: tick(clock))
    timer.start(1000)

    exit_code = app.exec_()

    return exit_code

def tick(clock: ClockWidget):
    now = datetime.datetime.now()
    clock.set_time(now.hour, now.minute, now.second)

def sigint(sig, frame):
    sys.stdout.write("\nexit\n")
    sys.exit(0)

if __name__ == '__main__':
    sys.exit(main())

