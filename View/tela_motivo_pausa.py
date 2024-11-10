# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'View/tela_motivo_pausa.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TelaMotivoPausa(object):
    def setupUi(self, TelaMotivoPausa):
        TelaMotivoPausa.setObjectName("TelaMotivoPausa")
        TelaMotivoPausa.resize(1024, 768)
        self.label = QtWidgets.QLabel(TelaMotivoPausa)
        self.label.setGeometry(QtCore.QRect(300, 50, 361, 40))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(TelaMotivoPausa)
        self.groupBox.setGeometry(QtCore.QRect(110, 200, 801, 361))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.rbtDescanso = QtWidgets.QRadioButton(self.groupBox)
        self.rbtDescanso.setGeometry(QtCore.QRect(40, 70, 311, 30))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.rbtDescanso.setFont(font)
        self.rbtDescanso.setObjectName("rbtDescanso")
        self.rbtTrocaTurno = QtWidgets.QRadioButton(self.groupBox)
        self.rbtTrocaTurno.setGeometry(QtCore.QRect(40, 120, 311, 30))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.rbtTrocaTurno.setFont(font)
        self.rbtTrocaTurno.setObjectName("rbtTrocaTurno")
        self.rbtHoraAlmoco = QtWidgets.QRadioButton(self.groupBox)
        self.rbtHoraAlmoco.setGeometry(QtCore.QRect(40, 170, 311, 30))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.rbtHoraAlmoco.setFont(font)
        self.rbtHoraAlmoco.setObjectName("rbtHoraAlmoco")
        self.rbtFinalExpediente = QtWidgets.QRadioButton(self.groupBox)
        self.rbtFinalExpediente.setGeometry(QtCore.QRect(40, 220, 311, 30))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.rbtFinalExpediente.setFont(font)
        self.rbtFinalExpediente.setObjectName("rbtFinalExpediente")
        self.btVoltar = QtWidgets.QPushButton(TelaMotivoPausa)
        self.btVoltar.setGeometry(QtCore.QRect(104, 630, 212, 102))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btVoltar.setFont(font)
        self.btVoltar.setObjectName("btVoltar")
        self.btOK = QtWidgets.QPushButton(TelaMotivoPausa)
        self.btOK.setGeometry(QtCore.QRect(704, 630, 212, 102))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btOK.setFont(font)
        self.btOK.setObjectName("btOK")

        self.retranslateUi(TelaMotivoPausa)
        QtCore.QMetaObject.connectSlotsByName(TelaMotivoPausa)

    def retranslateUi(self, TelaMotivoPausa):
        _translate = QtCore.QCoreApplication.translate
        TelaMotivoPausa.setWindowTitle(_translate("TelaMotivoPausa", "Form"))
        self.label.setText(_translate("TelaMotivoPausa", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">MOTIVO DA PAUSA</span></p></body></html>"))
        self.groupBox.setTitle(_translate("TelaMotivoPausa", "Escolha um motivo para a pausa"))
        self.rbtDescanso.setText(_translate("TelaMotivoPausa", "Descanso"))
        self.rbtTrocaTurno.setText(_translate("TelaMotivoPausa", "Troca de turno"))
        self.rbtHoraAlmoco.setText(_translate("TelaMotivoPausa", "Hora de Almoço"))
        self.rbtFinalExpediente.setText(_translate("TelaMotivoPausa", "Final de espediente"))
        self.btVoltar.setText(_translate("TelaMotivoPausa", "VOLTAR"))
        self.btOK.setText(_translate("TelaMotivoPausa", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TelaMotivoPausa = QtWidgets.QWidget()
    ui = Ui_TelaMotivoPausa()
    ui.setupUi(TelaMotivoPausa)
    TelaMotivoPausa.show()
    sys.exit(app.exec_())
