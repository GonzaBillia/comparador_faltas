# -*- coding: utf-8 -*-
#
# Form implementation generated from reading ui file '.\ui\design.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Reporter de Faltas")
        MainWindow.resize(411, 340)  # Aumentamos la altura para incluir nuevos controles
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Sección para el archivo ZIP
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 331, 21))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 60, 231, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 60, 81, 23))
        self.pushButton.setObjectName("pushButton")
        
        # Sección para el archivo CSV
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 100, 331, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 130, 231, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 130, 81, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        
        # Sección para seleccionar el destino del archivo procesado
        self.label_destination = QtWidgets.QLabel(self.centralwidget)
        self.label_destination.setGeometry(QtCore.QRect(40, 170, 331, 21))
        self.label_destination.setObjectName("label_destination")
        self.lineEdit_destination = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_destination.setGeometry(QtCore.QRect(40, 200, 231, 20))
        self.lineEdit_destination.setObjectName("lineEdit_destination")
        self.pushButton_destination = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_destination.setGeometry(QtCore.QRect(290, 200, 81, 23))
        self.pushButton_destination.setObjectName("pushButton_destination")
        
        # Botón para procesar
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(130, 260, 141, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Selecciona el archivo ZIP de Pedidos de Sucursal:"))
        self.pushButton.setText(_translate("MainWindow", "Seleccionar"))
        self.label_2.setText(_translate("MainWindow", "Selecciona el Archivo CSV de Pedidos Intersucursal:"))
        self.pushButton_2.setText(_translate("MainWindow", "Seleccionar"))
        self.label_destination.setText(_translate("MainWindow", "Selecciona el destino del archivo procesado:"))
        self.pushButton_destination.setText(_translate("MainWindow", "Seleccionar"))
        self.pushButton_3.setText(_translate("MainWindow", "Procesar"))
