from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Model.ViewRotina import TelaViewRotina
from View.tela_op import Ui_TelaOP
from Controller.Teclados import AlphanumericKeyboard, NumericKeyboard
from Model.ViewReceita import TelaViewReceita

class TelaOP(QDialog):
    def __init__(self, dado=None, io=None, db=None, rotina=None):
        super().__init__()

        self.io = io
        self.dado = dado
        self.database = db
        self.dado.set_telas(self.dado.TELA_OP)
        self.rotina = rotina

        # Configuração da interface do usuário gerada pelo Qt Designer
        self.ui = Ui_TelaOP()
        self.ui.setupUi(self)

        # Remover a barra de título e ocultar os botões de maximizar e minimizar
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowState.WindowMaximized)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Maximizar a janela
        # self.showMaximized()
        if self.dado.full_scream == True:
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        self.ui.btVoltar.clicked.connect(self.voltar) # Voltar para a tela inicial
        self.ui.btAbrirEsquerdo.clicked.connect(self.abrir_esquerdo) # Abrir a receita
        self.ui.btAbrirDireito.clicked.connect(self.abrir_direito) # Abrir a receita

        self.ui.txNomeOP_Esquerdo.mousePressEvent = self.preenche_nome_op_esquerdo
        self.ui.txNomeOP_Direito.mousePressEvent = self.preenche_nome_op_direito
        self.ui.txQuantidadeOP_Esquerdo.mousePressEvent = self.preenche_qtd_op_esquerdo
        self.ui.txQuantidadeOP_Direito.mousePressEvent = self.preenche_qtd_op_direito
        self.ui.txMaterialPeca.mousePressEvent = self.carrega_peca

        self.ui.cbxLadoEsquerdo.stateChanged.connect(self.lado_esquerdo)
        self.ui.cbxLadoDireito.stateChanged.connect(self.lado_direito)

    def lado_esquerdo(self):
        self.desabilita_habilita_esquerdo(self.ui.cbxLadoEsquerdo.isChecked())
    
    def lado_direito(self):
        self.desabilita_habilita_direito(self.ui.cbxLadoDireito.isChecked())

    def preenche_nome_op_esquerdo(self, event):
        teclado = AlphanumericKeyboard(dado=self.dado)
        teclado.exec_()
        self.ui.txNomeOP_Esquerdo.setText(teclado.line_edit.text())

    def preenche_qtd_op_esquerdo(self, event):
        teclado = NumericKeyboard(dado=self.dado)
        teclado.exec_()
        self.ui.txQuantidadeOP_Esquerdo.setText(teclado.line_edit.text())

    def preenche_nome_op_direito(self, event):
        teclado = AlphanumericKeyboard(dado=self.dado)
        teclado.exec_()
        self.ui.txNomeOP_Direito.setText(teclado.line_edit.text())

    def preenche_qtd_op_direito(self, event):
        teclado = NumericKeyboard(dado=self.dado)
        teclado.exec_()
        self.ui.txQuantidadeOP_Direito.setText(teclado.line_edit.text())

    def carrega_peca(self, event):
        receita = TelaViewReceita(dado=self.dado, io=self.io, db=self.database, rotina=self.rotina, target=self.dado.TELA_OP)
        receita.setModal(True)
        receita.exec_()
        self.ui.txMaterialPeca.setText(receita.nome_programa)
        
    def desabilita_habilita_esquerdo(self, estado):
        self.ui.txNomeOP_Esquerdo.setEnabled(estado)
        self.ui.txQuantidadeOP_Esquerdo.setEnabled(estado)
        self.ui.btAbrirEsquerdo.setEnabled(estado)
        if estado == False:
            self.ui.txNomeOP_Esquerdo.setText("")
            self.ui.txQuantidadeOP_Esquerdo.setText("")

    def desabilita_habilita_direito(self, estado):
        self.ui.txNomeOP_Direito.setEnabled(estado)
        self.ui.txQuantidadeOP_Direito.setEnabled(estado)
        self.ui.btAbrirDireito.setEnabled(estado)
        if estado == False:
            self.ui.txNomeOP_Direito.setText("")
            self.ui.txQuantidadeOP_Direito.setText("")


    def abrir_esquerdo(self):
        self.dado.set_telas(self.dado.TELA_RECEITA_VIEW)
        view_rotina = TelaViewRotina(dado=self.dado, io=self.io, db=self.database, rotina=self.rotina, target=self.dado.TELA_OP)
        view_rotina.setModal(True)
        view_rotina.exec_()
        self.ui.txNomeOP_Esquerdo.setText(view_rotina.nome_programa)

    def abrir_direito(self):
        self.dado.set_telas(self.dado.TELA_RECEITA_VIEW)
        view_rotina = TelaViewRotina(dado=self.dado, io=self.io, db=self.database, rotina=self.rotina, target=self.dado.TELA_OP)
        view_rotina.setModal(True)
        view_rotina.exec_()
        self.ui.txNomeOP_Direito.setText(view_rotina.nome_programa)

    def voltar(self):
        self.close()
    
    def closeEvent(self, event):
        event.accept()