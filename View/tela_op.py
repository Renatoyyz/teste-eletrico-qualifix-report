# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'View/tela_op.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TelaOP(object):
    def setupUi(self, TelaOP):
        TelaOP.setObjectName("TelaOP")
        TelaOP.resize(1024, 768)
        self.btVoltar = QtWidgets.QPushButton(TelaOP)
        self.btVoltar.setGeometry(QtCore.QRect(53, 630, 212, 102))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btVoltar.setFont(font)
        self.btVoltar.setObjectName("btVoltar")
        self.btOk = QtWidgets.QPushButton(TelaOP)
        self.btOk.setGeometry(QtCore.QRect(770, 630, 210, 102))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btOk.setFont(font)
        self.btOk.setObjectName("btOk")
        self.label = QtWidgets.QLabel(TelaOP)
        self.label.setGeometry(QtCore.QRect(60, 30, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(TelaOP)
        self.label_2.setGeometry(QtCore.QRect(60, 140, 391, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(TelaOP)
        self.label_3.setGeometry(QtCore.QRect(320, 250, 410, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.txNomeOP_Esquerdo = QtWidgets.QLineEdit(TelaOP)
        self.txNomeOP_Esquerdo.setGeometry(QtCore.QRect(60, 70, 411, 40))
        self.txNomeOP_Esquerdo.setObjectName("txNomeOP_Esquerdo")
        self.txQuantidadeOP_Esquerdo = QtWidgets.QLineEdit(TelaOP)
        self.txQuantidadeOP_Esquerdo.setGeometry(QtCore.QRect(60, 180, 410, 40))
        self.txQuantidadeOP_Esquerdo.setObjectName("txQuantidadeOP_Esquerdo")
        self.txMaterialPeca = QtWidgets.QLineEdit(TelaOP)
        self.txMaterialPeca.setGeometry(QtCore.QRect(320, 290, 411, 40))
        self.txMaterialPeca.setObjectName("txMaterialPeca")
        self.groupBox = QtWidgets.QGroupBox(TelaOP)
        self.groupBox.setGeometry(QtCore.QRect(54, 450, 920, 121))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.groupBox.setFont(font)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.cbxLadoEsquerdo = QtWidgets.QCheckBox(self.groupBox)
        self.cbxLadoEsquerdo.setGeometry(QtCore.QRect(20, 40, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cbxLadoEsquerdo.setFont(font)
        self.cbxLadoEsquerdo.setChecked(True)
        self.cbxLadoEsquerdo.setObjectName("cbxLadoEsquerdo")
        self.cbxLadoDireito = QtWidgets.QCheckBox(self.groupBox)
        self.cbxLadoDireito.setGeometry(QtCore.QRect(517, 40, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cbxLadoDireito.setFont(font)
        self.cbxLadoDireito.setChecked(True)
        self.cbxLadoDireito.setObjectName("cbxLadoDireito")
        self.txNomeOP_Direito = QtWidgets.QLineEdit(TelaOP)
        self.txNomeOP_Direito.setGeometry(QtCore.QRect(563, 70, 411, 40))
        self.txNomeOP_Direito.setObjectName("txNomeOP_Direito")
        self.label_4 = QtWidgets.QLabel(TelaOP)
        self.label_4.setGeometry(QtCore.QRect(563, 140, 391, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.txQuantidadeOP_Direito = QtWidgets.QLineEdit(TelaOP)
        self.txQuantidadeOP_Direito.setGeometry(QtCore.QRect(563, 180, 410, 40))
        self.txQuantidadeOP_Direito.setObjectName("txQuantidadeOP_Direito")
        self.label_6 = QtWidgets.QLabel(TelaOP)
        self.label_6.setGeometry(QtCore.QRect(563, 30, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.btAbrirEsquerdo = QtWidgets.QPushButton(TelaOP)
        self.btAbrirEsquerdo.setGeometry(QtCore.QRect(54, 370, 212, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btAbrirEsquerdo.setFont(font)
        self.btAbrirEsquerdo.setObjectName("btAbrirEsquerdo")
        self.btAbrirDireito = QtWidgets.QPushButton(TelaOP)
        self.btAbrirDireito.setGeometry(QtCore.QRect(767, 370, 212, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btAbrirDireito.setFont(font)
        self.btAbrirDireito.setObjectName("btAbrirDireito")

        self.retranslateUi(TelaOP)
        QtCore.QMetaObject.connectSlotsByName(TelaOP)

    def retranslateUi(self, TelaOP):
        _translate = QtCore.QCoreApplication.translate
        TelaOP.setWindowTitle(_translate("TelaOP", "Form"))
        self.btVoltar.setText(_translate("TelaOP", "VOLTAR"))
        self.btOk.setText(_translate("TelaOP", "OK"))
        self.label.setText(_translate("TelaOP", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">NÚMERO DE ORDEM DE PRODUÇÃO</span></p></body></html>"))
        self.label_2.setText(_translate("TelaOP", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">QUANTIDADE A PRODUZIR</span></p></body></html>"))
        self.label_3.setText(_translate("TelaOP", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">MATERIAL - PEÇA</span></p></body></html>"))
        self.groupBox.setTitle(_translate("TelaOP", "Peças"))
        self.cbxLadoEsquerdo.setText(_translate("TelaOP", "Lado Esquerdo"))
        self.cbxLadoDireito.setText(_translate("TelaOP", "Lado Direito"))
        self.label_4.setText(_translate("TelaOP", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">QUANTIDADE A PRODUZIR</span></p></body></html>"))
        self.label_6.setText(_translate("TelaOP", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">NÚMERO DE ORDEM DE PRODUÇÃO</span></p></body></html>"))
        self.btAbrirEsquerdo.setText(_translate("TelaOP", "ABRIR"))
        self.btAbrirDireito.setText(_translate("TelaOP", "ABRIR"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TelaOP = QtWidgets.QWidget()
    ui = Ui_TelaOP()
    ui.setupUi(TelaOP)
    TelaOP.show()
    sys.exit(app.exec_())
