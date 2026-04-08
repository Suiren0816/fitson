from __future__ import annotations

from PySide6.QtCore import QPointF, QRect, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


class CompassOverlay(QWidget):
    """Small overlay widget showing the displayed-image axis directions.

    Owned by `ImageCanvas`. The compass paints two arrows representing the
    direction of the original-image +X and +Y axes after the current
    orientation transform has been applied.
    """

    SIZE = 84

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._x_axis: tuple[float, float] = (1.0, 0.0)
        self._y_axis: tuple[float, float] = (0.0, 1.0)
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    def set_axes(self, x_axis: tuple[float, float], y_axis: tuple[float, float]) -> None:
        self._x_axis = x_axis
        self._y_axis = y_axis
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: ANN001
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        bg = QColor(0, 0, 0, 140)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg)
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 8, 8)

        center = QPointF(self.width() / 2.0, self.height() / 2.0)
        length = self.SIZE * 0.32

        self._draw_arrow(painter, center, self._x_axis, length, QColor(255, 80, 80), "X")
        self._draw_arrow(painter, center, self._y_axis, length, QColor(80, 200, 255), "Y")

    def _draw_arrow(
        self,
        painter: QPainter,
        center: QPointF,
        axis: tuple[float, float],
        length: float,
        color: QColor,
        label: str,
    ) -> None:
        ax, ay = axis
        end = QPointF(center.x() + ax * length, center.y() + ay * length)

        pen = QPen(color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(center, end)

        # Arrow head: two short lines perpendicular to axis at end point
        head = length * 0.25
        # Perp vector
        px, py = -ay, ax
        h1 = QPointF(end.x() - ax * head + px * head * 0.6, end.y() - ay * head + py * head * 0.6)
        h2 = QPointF(end.x() - ax * head - px * head * 0.6, end.y() - ay * head - py * head * 0.6)
        painter.drawLine(end, h1)
        painter.drawLine(end, h2)

        # Label slightly past arrow head
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        label_pos = QPointF(end.x() + ax * 10 - 5, end.y() + ay * 10 + 4)
        painter.drawText(label_pos, label)
