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



import os
from PyQt5 import QtCore, QtGui, QtWidgets

from lib.unidades import Currency, getrates
from UI.delegate import CellEditor
from lib.config import conf_dir


class UI_conversorUnidades(QtWidgets.QDialog):
    def __init__(self, unidad, valor=None, parent=None):
        super(UI_conversorUnidades, self).__init__(parent)
        self.unidad = unidad
        self.magnitud = unidad.__name__
        self.texto = unidad.__text__
        self.unit = unidad.__units__
        if unidad.__tooltip__:
            self.tooltip = unidad.__tooltip__
        else:
            self.tooltip = unidad.__text__
        self.value = self.unidad(valor)
        self.setWindowTitle(unidad.__title__)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.tabla = QtWidgets.QTableWidget()
        self.tabla.setRowCount(len(self.texto))
        self.tabla.setColumnCount(1)
        self.tabla.setItemDelegateForColumn(0, CellEditor(self))
        self.tabla.horizontalHeader().setVisible(False)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        if self.magnitud in ["SpecificVolume", "Density", "MassFlow", "VolFlow", "ThermalConductivity", "HeatTransfCoef"]:
            self.resize(215, self.minimumHeight())
        elif self.magnitud == "Currency":
            self.resize(250, 500)
        else:
            self.resize(self.minimumSize())

        if self.magnitud in ["Temperature", "Area", "Volume",  "Length", "Angle", "Time"]:
            x = 15
        elif self.magnitud in["ThermalConductivity"]:
            x = 10
        elif self.magnitud in ["Speed", "Mass", "Acceleration", "Energy", "Enthalpy", "MassFlow", "Diffusivity", "Tension", "Solubility_parameter", "HeatTransfCoef"]:
            x = 5
        else:
            x = 0
        self.gridLayout.addItem(QtWidgets.QSpacerItem(x,15,QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed),2,0)
        self.gridLayout.addItem(QtWidgets.QSpacerItem(x,15,QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed),2,2)

        for i in range(len(self.texto)):
            self.tabla.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(self.texto[i]))
            self.tabla.setRowHeight(i,24)
            self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(""))
            self.tabla.item(i, 0).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        for i in range(len(self.tooltip)):
            self.tabla.item(i, 0).setToolTip(QtWidgets.QApplication.translate("pychemqt", self.tooltip[i]))

        if valor:
            self.rellenarTabla(self.value)
            self.tabla.resizeColumnsToContents()
        if self.magnitud!="Currency":
            self.tabla.setFixedHeight(len(self.texto)*24+4)
        self.gridLayout.addWidget(self.tabla, 2, 1, 1, 1)
        self.tabla.cellChanged.connect(self.actualizar)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox,3,0,1,3)

    def rellenarTabla(self, valor):
        for i, key in enumerate(self.unit):
            self.tabla.item(i, 0).setText(valor.format(key))

    def actualizar(self, fila, columna):
        self.tabla.blockSignals(True)
        self.value=self.unidad(float(self.tabla.item(fila, columna).text()), self.unit[fila])
        self.rellenarTabla(self.value)
        self.tabla.blockSignals(False)


class moneda(UI_conversorUnidades):

    def __init__(self, valor=None, parent=None):
        super(moneda, self).__init__(Currency, valor=valor, parent=parent)

        self.fecha = QtWidgets.QLabel(QtWidgets.QApplication.translate(
            "pychemqt", "Date::") + self.value.fecha)
        self.gridLayout.addWidget(self.fecha, 0, 1)
        self.botonActualizar = QtWidgets.QPushButton(
            QtWidgets.QApplication.translate("pychemqt", "Update"))
        self.botonActualizar.clicked.connect(self.getrates)
        self.gridLayout.addWidget(self.botonActualizar, 1, 1)

        for i in range(len(Currency.__units__)):
            self.tabla.verticalHeaderItem(i).setIcon(QtGui.QIcon(QtGui.QPixmap(
                os.environ["pychemqt"]+"/images/flag/%s.gif" % Currency.__units__[i])))

    def getrates(self):
        filename = conf_dir+"moneda.dat"
        getrates(filename)
        self.value = self.unidad(self.value)
        self.fecha.setText(QtWidgets.QApplication.translate("pychemqt", "Date:") +
                           self.value.fecha)
        if self.value != 0:
            self.actualizar(0, 0)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogo = moneda(300)
    dialogo.show()
    sys.exit(app.exec_())
