from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from View.tela_motivo_pausa import Ui_TelaMotivoPausa


class MotivoPausa(QDialog):
    def __init__(self, dado=None, io=None, db=None, rotina=None):
        super().__init__()

        self.io = io
        self.dado = dado
        self.database = db
        self.rotina = rotina
        self.motivo_pausa = None

        self.ui = Ui_TelaMotivoPausa()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        if self.dado.full_scream == True:
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        self.ui.btVoltar.clicked.connect(self.voltar)

        self.ui.rbtDescanso.clicked.connect( lambda: self.seleciona_motivo(self.ui.rbtDescanso.text()) )
        self.ui.rbtTrocaTurno.clicked.connect( lambda: self.seleciona_motivo(self.ui.rbtTrocaTurno.text()) )
        self.ui.rbtHoraAlmoco.clicked.connect( lambda: self.seleciona_motivo(self.ui.rbtHoraAlmoco.text()) )
        self.ui.rbtFinalExpediente.clicked.connect( lambda: self.seleciona_motivo(self.ui.rbtFinalExpediente.text()) )

    def seleciona_motivo(self, motivo):
        self.motivo_pausa = motivo
        self.close()

    def voltar(self):
        self.motivo_pausa = None
        self.close()

    def closeEvent(self, event):
        event.accept()

    