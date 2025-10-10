# coding:utf-8
from typing import Union

from PyQt6.QtCore import pyqtSignal, QUrl, Qt, QRectF, QSize, QPoint, pyqtProperty, QRect
from PyQt6.QtGui import QDesktopServices, QIcon, QPainter, QColor, QPainterPath
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QRadioButton, QToolButton, QApplication, QWidget, QSizePolicy

from ...common.animation import TranslateYAnimation
from ...common.icon import FluentIconBase, drawIcon, isDarkTheme, Theme, toQIcon, Icon
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont, getFont
from ...common.style_sheet import FluentStyleSheet, themeColor, ThemeColor
from ...common.color import autoFallbackThemeColor
from ...common.overload import singledispatchmethod
from .menu import RoundMenu, MenuAnimationType

class RadioButton(QRadioButton):
    """Radio button

    Constructors
    ------------
    * RadioButton(`parent`: QWidget = None)
    * RadioButton(`url`: text, `text`: str, `parent`: QWidget = None,
                  `icon`: QIcon | str | FluentIconBase = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._lightTextColor = QColor(0, 0, 0)
        self._darkTextColor = QColor(255, 255, 255)
        self.lightIndicatorColor = QColor()
        self.darkIndicatorColor = QColor()
        self.indicatorPos = QPoint(11, 12)
        self.isHover = False

        FluentStyleSheet.BUTTON.apply(self)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def _postInit(self):
        pass

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self._drawIndicator(painter)
        self._drawText(painter)

    def _drawText(self, painter: QPainter):
        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setFont(self.font())
        painter.setPen(self.textColor())
        painter.drawText(QRect(29, 0, self.width(), self.height()), Qt.AlignmentFlag.AlignVCenter, self.text())

    def _drawIndicator(self, painter: QPainter):
        if self.isChecked():
            if self.isEnabled():
                borderColor = autoFallbackThemeColor(self.lightIndicatorColor, self.darkIndicatorColor)
            else:
                borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 55)

            filledColor = Qt.GlobalColor.black if isDarkTheme() else Qt.GlobalColor.white

            if self.isHover and not self.isDown():
                self._drawCircle(painter, self.indicatorPos, 10, 4, borderColor, filledColor)
            else:
                self._drawCircle(painter, self.indicatorPos, 10, 5, borderColor, filledColor)

        else:
            if self.isEnabled():
                if not self.isDown():
                    borderColor = QColor(255, 255, 255, 153) if isDarkTheme() else QColor(0, 0, 0, 153)
                else:
                    borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 55)

                if self.isDown():
                    filledColor = Qt.GlobalColor.black if isDarkTheme() else Qt.GlobalColor.white
                elif self.isHover:
                    filledColor = QColor(255, 255, 255, 11) if isDarkTheme() else QColor(0, 0, 0, 15)
                else:
                    filledColor = QColor(0, 0, 0, 26) if isDarkTheme() else QColor(0, 0, 0, 6)
            else:
                filledColor = Qt.GlobalColor.transparent
                borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 55)

            self._drawCircle(painter, self.indicatorPos, 10, 1, borderColor, filledColor)

            if self.isEnabled() and self.isDown():
                borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 24)
                self._drawCircle(painter, self.indicatorPos, 9, 4, borderColor, Qt.GlobalColor.transparent)

    def _drawCircle(self, painter: QPainter, center: QPoint, radius, thickness, borderColor, filledColor):
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)

        # outer circle (border)
        outerRect = QRectF(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)
        path.addEllipse(outerRect)

        # inner center (filled)
        ir = radius - thickness
        innerRect = QRectF(center.x() - ir, center.y() - ir, 2 * ir, 2 * ir)
        innerPath = QPainterPath()
        innerPath.addEllipse(innerRect)

        path = path.subtracted(innerPath)

        # draw outer ring
        painter.setPen(Qt.PenStyle.NoPen)
        painter.fillPath(path, borderColor)

        # fill inner circle
        painter.fillPath(innerPath, filledColor)

    def textColor(self):
        return self.darkTextColor if isDarkTheme() else self.lightTextColor

    def getLightTextColor(self) -> QColor:
        return self._lightTextColor

    def getDarkTextColor(self) -> QColor:
        return self._darkTextColor

    def setLightTextColor(self, color: QColor):
        self._lightTextColor = QColor(color)
        self.update()

    def setDarkTextColor(self, color: QColor):
        self._darkTextColor = QColor(color)
        self.update()

    def setIndicatorColor(self, light, dark):
        self.lightIndicatorColor = QColor(light)
        self.darkIndicatorColor = QColor(dark)
        self.update()

    def setTextColor(self, light, dark):
        self.setLightTextColor(light)
        self.setDarkTextColor(dark)

    lightTextColor = pyqtProperty(QColor, getLightTextColor, setLightTextColor)
    darkTextColor = pyqtProperty(QColor, getDarkTextColor, setDarkTextColor)
