from datetime import datetime
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from Model.ViewRotina import TelaViewRotina
from View.tela_op import Ui_TelaOP
from Controller.Teclados import AlphanumericKeyboard, NumericKeyboard
from Model.ViewReceita import TelaViewReceita
from Controller.Message import SimpleMessageBox, MessageBox

class TelaOP(QDialog):
    def __init__(self, dado=None, io=None, db=None, rotina=None):
        super().__init__()

        self.io = io
        self.dado = dado
        self.database = db
        self.dado.set_telas(self.dado.TELA_OP)
        self.rotina = rotina

        self.nome_ordem_producao_esquerdo = None # Nome da ordem de produção esquerdo
        self.nome_ordem_producao_direito = None # Nome da ordem de produção direito
        self.id_esquerdo = None # ID da ordem de produção esquerdo
        self.id_direito = None # ID da ordem de produção direito

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
        self.ui.btOk.clicked.connect(self.salvar_op) # Salvar a ordem de produção

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
        teclado = NumericKeyboard(dado=self.dado, type='int')
        teclado.exec_()
        self.ui.txQuantidadeOP_Esquerdo.setText(teclado.line_edit.text())

    def preenche_nome_op_direito(self, event):
        teclado = AlphanumericKeyboard(dado=self.dado)
        teclado.exec_()
        self.ui.txNomeOP_Direito.setText(teclado.line_edit.text())

    def preenche_qtd_op_direito(self, event):
        teclado = NumericKeyboard(dado=self.dado, type='int')
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
        view_rotina = TelaViewRotina(dado=self.dado, io=self.io, db=self.database, rotina=self.rotina, target=self.dado.TELA_OP, esquerdo_direito='esquerdo')
        view_rotina.setModal(True)
        view_rotina.exec_()
        try:
            registros = self.database.get_all_records_op_by_ordem_producao_esquerdo_direito(view_rotina.nome_programa, 'esquerdo')
            self.id_esquerdo = registros[0][0]
            self.nome_ordem_producao_esquerdo = view_rotina.nome_programa
            if registros:
                registro = registros[0]
                if self.ui.txMaterialPeca.text() == "" or self.ui.txMaterialPeca.text() == registro[3]:
                    self.ui.txNomeOP_Esquerdo.setText(registro[1])
                    self.ui.txQuantidadeOP_Esquerdo.setText(str(registro[2]))
                    self.ui.txMaterialPeca.setText(registro[3])
                elif self.ui.txMaterialPeca.text() != registro[3]:
                    msg = SimpleMessageBox(title="Aviso")
                    msg.exec(msg="As duas peças são diferentes, escolha a mesma peça para os dois lados.")
                    
        except Exception as e:
            print(f"Erro ao abrir receita esquerdo: {e}")

    def abrir_direito(self):
        self.dado.set_telas(self.dado.TELA_RECEITA_VIEW)
        view_rotina = TelaViewRotina(dado=self.dado, io=self.io, db=self.database, rotina=self.rotina, target=self.dado.TELA_OP, esquerdo_direito='direito')    
        view_rotina.setModal(True)
        view_rotina.exec_()
        try:
            registros = self.database.get_all_records_op_by_ordem_producao_esquerdo_direito(view_rotina.nome_programa, 'direito')
            self.id_direito = registros[0][0]
            self.nome_ordem_producao_direito = view_rotina.nome_programa
            if registros:
                registro = registros[0]
                if self.ui.txMaterialPeca.text() == "" or self.ui.txMaterialPeca.text() == registro[3]:
                    self.ui.txNomeOP_Direito.setText(registro[1])
                    self.ui.txQuantidadeOP_Direito.setText(str(registro[2]))
                    self.ui.txMaterialPeca.setText(registro[3])
                elif self.ui.txMaterialPeca.text() != registro[3]:
                    msg = SimpleMessageBox(title="Aviso")
                    msg.exec(msg="As duas peças são diferentes, escolha a mesma peça para os dois lados.")
        except Exception as e:
            print(f"Erro ao abrir receita direito: {e}")

# Tarefa: Salvar a ordem de produção sem repetir o nome da ordem de produção
# Quando o usuário clicar no botão OK, o sistema deve verificar se o nome da ordem de produção já existe no banco de dados
# Se existir, o sistema deve exibir uma mensagem de erro e não salvar a ordem de produção
# Se não existir, o sistema deve salvar a ordem de produção
# O sistema deve salvar a ordem de produção para o lado esquerdo e para o lado direito
# Depois de salvar ou se ja existir, o sistema deve fechar a tela de ordem de produção e abrir a tela de ExecucaoPrograma com os parametros necessarios
    def salvar_op(self):
        receita_peca = self.ui.txMaterialPeca.text()
        login = self.dado.nome_login
        criado = datetime.now()
        finalizado = None
        fim_op = 0

        if self.ui.cbxLadoEsquerdo.isChecked():
            nome_op_esquerdo = self.ui.txNomeOP_Esquerdo.text()
            quantidade_op_esquerdo = self.ui.txQuantidadeOP_Esquerdo.text()
            if nome_op_esquerdo and quantidade_op_esquerdo and receita_peca:
                if not self.database.record_op_exists(nome_op_esquerdo, 'esquerdo'):
                    self.database.create_record_op(
                    nome_op_esquerdo, quantidade_op_esquerdo, receita_peca, 'esquerdo', login, criado, finalizado, fim_op
                    )
                    self.id_esquerdo = self.database.get_id_op(nome_op_esquerdo, 'esquerdo')
                else:
                    print("A ordem de produção esquerdo já existe.")

        if self.ui.cbxLadoDireito.isChecked():
            nome_op_direito = self.ui.txNomeOP_Direito.text()
            quantidade_op_direito = self.ui.txQuantidadeOP_Direito.text()
            if nome_op_direito and quantidade_op_direito and receita_peca:
                if not self.database.record_op_exists(nome_op_direito, 'direito'):
                    self.database.create_record_op(
                    nome_op_direito, quantidade_op_direito, receita_peca, 'direito', login, criado, finalizado, fim_op
                    )
                    self.id_direito = self.database.get_id_op(nome_op_direito, 'direito')
                else:
                    print("A ordem de produção direito já existe.")

        self.nome_ordem_producao_esquerdo = self.ui.txNomeOP_Esquerdo.text()
        self.nome_ordem_producao_direito = self.ui.txNomeOP_Direito.text()

    # A partir desse ponto, o sistema deve fechar a tela de ordem de produção e abrir a tela de ExecucaoPrograma, passando os parametros necessarios
    # A tela de ExecucaoPrograma deve ser reajustada para receber novo banco de dados e novos parametros
    # Corrigir em Database.py para criar tabelas de status de ordem de produção, tais como: motivo de parada, troca de operador, etc. 

    def voltar(self):
        self.close()
    
    def closeEvent(self, event):
        event.accept()