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

        self.retranslateUi(TelaMotivoPausa)
        QtCore.QMetaObject.connectSlotsByName(TelaMotivoPausa)

    def retranslateUi(self, TelaMotivoPausa):
        _translate = QtCore.QCoreApplication.translate
        TelaMotivoPausa.setWindowTitle(_translate("TelaMotivoPausa", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TelaMotivoPausa = QtWidgets.QWidget()
    ui = Ui_TelaMotivoPausa()
    ui.setupUi(TelaMotivoPausa)
    TelaMotivoPausa.show()
    sys.exit(app.exec_())
