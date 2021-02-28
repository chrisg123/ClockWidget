from math import sin,cos,pi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QSize, QPointF
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor

class ClockWidget(QWidget):
    def __init__(self, size: QSize=None, frame_ratio=0.1):
        super().__init__()
        if size is None: size = QSize(300,300)
        self.setFixedSize(size)

        self._center = QPointF(self.width() / 2.0, self.height() / 2.0)
        self._radius = (min(self.width(), self.height()) * 0.9) / 2
        self._frame_width = self._radius * frame_ratio
        self._inner_radius = self._radius - (self._frame_width / 2)

        self._sec_hand_width = max(1, self._frame_width * 0.1)
        self._sec_hand_length = self._inner_radius * 0.80
        self._sec_hand_pt = self._get_sec_hand_pt(0)

        self._min_hand_width = self._sec_hand_width * 3
        self._min_hand_length = self._sec_hand_length * 0.9
        self._min_hand_pt = self._get_min_hand_pt(0)

        self._hr_hand_width = self._sec_hand_width * 5
        self._hr_hand_length = self._sec_hand_length * 0.75
        self._hr_hand_pt = self._get_hr_hand_pt(0)

        self._hr_line_length = self._inner_radius * 0.10

        self._bgcolor = Qt.white
        self._fgcolor= Qt.black
        self._hr_hand_color = Qt.black
        self._min_hand_color = Qt.black
        self._sec_hand_color = Qt.black

    def set_background_color(self, color: QColor):
        self._bgcolor = color

    def set_foreground_color(self, color: QColor):
        self._fgcolor = color

    def set_hr_hand_color(self, color: QColor):
        self._hr_hand_color = color

    def set_min_hand_color(self, color: QColor):
        self._min_hand_color = color

    def set_sec_hand_color(self, color: QColor):
        self._sec_hand_color = color

    def set_time(self, hr: int, min:int, sec:int):
        if hr > 24: raise ValueError()
        if min > 59: raise ValueError()
        if sec > 59: raise ValueError()
        hr = hr % 12
        self._hr_hand_pt =  self._get_hr_hand_pt(((hr*60) + min)/60)
        self._min_hand_pt =  self._get_min_hand_pt( ((min*60) + sec) / 60 )
        self._sec_hand_pt =  self._get_sec_hand_pt(sec)

        self.update()

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter()
        painter.begin(self)

        if self._bgcolor is not None:
            bgcolor = self._bgcolor
            painter.setPen(QPen(self._bgcolor, 1, Qt.SolidLine))
            painter.setBrush(QBrush(self._bgcolor, Qt.SolidPattern))
            painter.drawRect(event.rect())

        painter.setPen(QPen(self._fgcolor, self._frame_width, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.transparent, Qt.SolidPattern))

        painter.setRenderHint(QPainter.Antialiasing)
        r = self._radius
        cnt = self._center
        painter.drawEllipse(cnt,r,r)

        painter.setPen(QPen(Qt.blue, 10, Qt.SolidLine))

        #draw hr indicators
        for i in range(0,12):
            deg = i * 30
            l = self._inner_radius *.97
            p1 = self._get_radial_pt(deg, l)
            p2 = self._get_radial_pt(deg, l - self._hr_line_length)

            painter.setPen(QPen(self._fgcolor, self._sec_hand_width, Qt.SolidLine))
            painter.drawLine(p1, p2)

        painter.setPen(QPen(self._hr_hand_color,self._hr_hand_width, Qt.SolidLine))
        painter.drawLine(cnt, self._hr_hand_pt)

        painter.setPen(QPen(self._min_hand_color,self._min_hand_width, Qt.SolidLine))
        painter.drawLine(cnt, self._min_hand_pt)

        painter.setPen(QPen(self._sec_hand_color, self._sec_hand_width, Qt.SolidLine))
        painter.drawLine(cnt, self._sec_hand_pt)

        r = (self._hr_hand_width / 2) * 1.2
        cnt = self._center
        painter.setBrush(QBrush(self._fgcolor, Qt.SolidPattern))
        painter.drawEllipse(cnt,r,r)

        painter.end()

    def _get_hr_hand_pt(self, hr: float) -> QPointF:
        deg_per_min = 0.5
        deg = deg_per_min * ((hr-3) % 12) * 60
        return self._get_radial_pt(deg, self._hr_hand_length)

    def _get_min_hand_pt(self, min: float) -> QPointF:
        deg_per_min = 0.1
        deg = deg_per_min * ((min-15) % 60) * 60
        return self._get_radial_pt(deg, self._min_hand_length)

    def _get_sec_hand_pt(self, sec: float) -> QPointF:
        deg_per_sec = 0.1
        deg = deg_per_sec * ((sec-15) % 60) * 60
        return self._get_radial_pt(deg, self._sec_hand_length)

    def _get_radial_pt(self, deg: float, l: int):
        c = self._center
        radians = (deg * pi) / 180
        x_ = cos(radians) * l
        y_ = sin(radians) * l
        return QPointF(c.x() + x_, c.y() + y_)
