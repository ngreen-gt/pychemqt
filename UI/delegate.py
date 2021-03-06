#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2016, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


###############################################################################
# Module to implement delegate special editiing in tables
#   -CellEditor
#   -SpinEditor
#   -CheckEditor
#   -SpinEditor
#   -LineStyleDelegate
#   -comboLine
###############################################################################


import os
from PyQt5 import QtCore, QtGui, QtWidgets


class CellEditor(QtWidgets.QItemDelegate):
    """Numeric editor of tableitem, with numeric validator"""
    def __init__(self, parent=None):
        super(CellEditor, self).__init__(parent)

    def createEditor(self, parent, option, index):
        widget = QtWidgets.QLineEdit(parent)
        widget.setAlignment(QtCore.Qt.AlignRight)
        validator = QtGui.QDoubleValidator(self)
        locale = QtCore.QLocale("en")
        validator.setLocale(locale)
        widget.setValidator(validator)
        return widget


class SpinEditor(QtWidgets.QItemDelegate):
    """Spinbox editor for tableitem"""
    def __init__(self, parent=None):
        super(SpinEditor, self).__init__(parent)

    def createEditor(self, parent, option, index):
        widget = QtWidgets.QSpinBox(parent)
        widget.setAlignment(QtCore.Qt.AlignRight)
        widget.setMinimum(1)
        return widget


class CheckEditor(QtWidgets.QItemDelegate):
    """Checkbox editor for tableitem"""
    def __init__(self, parent=None):
        super(CheckEditor, self).__init__(parent)

    def createEditor(self, parent, option, index):
        widget = QtWidgets.QCheckBox(parent)
        return widget

    def setEditorData(self, editor, index):
        value = bool(index.data(QtCore.Qt.DisplayRole))
        editor.setChecked(value)

    def setModelData(self, editor, model, index):
        value = editor.isChecked()
        model.setData(index, QtCore.QVariant(value), QtCore.Qt.DisplayRole)


class ComboEditor(QtWidgets.QItemDelegate):
    """Combobox Editor for tableitem"""
    def __init__(self, owner, items=None):
        super(ComboEditor, self).__init__(owner)
        self.setItems(items)

    def setItems(self, items):
        self.items = items

    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QComboBox(parent)
        self.editor.addItems(self.items)
        return self.editor

    def setEditorData(self, editor, index):
        value = str(index.data(QtCore.Qt.DisplayRole).toString())
        try:
            num = self.items.index(value)
        except ValueError:
            num = -1
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, QtCore.QVariant(value), QtCore.Qt.DisplayRole)


class LineStyleDelegate(QtWidgets.QItemDelegate):
    """Special combobox editor delegate for line Style"""
    def __init__(self, object, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        data = index.model().data(index, QtCore.Qt.UserRole)
        if data.isValid() and data.toPyObject() is not None:
            data = data.toPyObject()
            painter.save()

            rect = option.rect
            rect.adjust(+5, 0, -5, 0)

            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.black)
            pen.setWidth(3)
            pen.setStyle(data)
            painter.setPen(pen)

            middle = (rect.bottom() + rect.top()) / 2
            painter.drawLine(rect.left(), middle, rect.right(), middle)
            painter.restore()

        else:
            QtWidgets.QItemDelegate.paint(self, painter, option, index)


class comboLine(QtWidgets.QComboBox):
    """Special combobox editor delegate for line Style"""
    def __init__(self, parent=None):
        QtWidgets.QComboBox.__init__(self, parent)
        lineas = [
            os.environ["pychemqt"]+"/images/button/solid_line.png",
            os.environ["pychemqt"]+"/images/button/dot_line.png",
            os.environ["pychemqt"]+"/images/button/dash_line.png",
            os.environ["pychemqt"]+"/images/button/dash_dot_line.png",
            os.environ["pychemqt"]+"/images/button/dash_dot_dot_line.png"]
        for i in lineas:
            self.addItem(QtGui.QIcon(QtGui.QPixmap(i)), "")
        self.setItemDelegate(LineStyleDelegate(self))

    def paintEvent(self, e):
        data = self.itemData(self.currentIndex(), QtCore.Qt.UserRole)
        if data.isValid() and data.toPyObject() is not None:
            data = data.toPyObject()
            p = QtWidgets.QStylePainter(self)
            p.setPen(self.palette().color(QtGui.QPalette.Text))

            opt = QtWidgets.QStyleOptionComboBox()
            self.initStyleOption(opt)
            p.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt)

            painter = QtGui.QPainter(self)
            painter.save()

            rect = p.style().subElementRect(
                QtWidgets.QStyle.SE_ComboBoxFocusRect, opt, self)
            rect.adjust(+5, 0, -5, 0)

            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.black)
            pen.setWidth(3)
            pen.setStyle(data)
            painter.setPen(pen)

            middle = (rect.bottom() + rect.top()) / 2
            painter.drawLine(rect.left(), middle, rect.right(), middle)
#            painter.restore()

        else:
            QtWidgets.QComboBox.paintEvent(self, e)
