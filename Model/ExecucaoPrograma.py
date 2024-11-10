from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QDateTime, Qt, QCoreApplication, QEvent, pyqtSignal, QThread, pyqtSlot, QMetaObject, Q_ARG
from datetime import datetime
from Controller.Message import MessageBox, SimpleMessageBox
from Controller.OpenFile import OpenFile
from View.tela_execucao_programa import Ui_TelaExecucao
from Model.MotivoPausa import MotivoPausa

import logging

# Configuração do logging
logging.basicConfig(filename='execucao_programa.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class Atualizador(QThread):
    sinal_atualizar = pyqtSignal(str)

    def __init__(self, operacao):
        super().__init__()
        self.operacao = operacao
        self._running = True

    def run(self):
        while self._running:
            QApplication.processEvents()  # Mantém a UI responsiva após iniciar as threads
            try:
                data_hora = QDateTime.currentDateTime()
                data_formatada = data_hora.toString('dd/MM/yyyy HH:mm:ss')
                self.sinal_atualizar.emit(data_formatada)
                self.msleep(100)
            except Exception as e:
                logging.error(f"Erro na thread Atualizador: {e}")
                self._running = False
            self.msleep(100)

    def iniciar(self):
        self._running = True
        self.start()
    def parar(self):
        self._running = False

class ExecutaRotinaThread(QThread):
    sinal_execucao = pyqtSignal(list,list,list,list)# Inicializa com a quantidade de variáveis que se deseja

    def __init__(self, operacao):
        super().__init__()
        self.operacao = operacao
        self._running = True
        self.esquerda_ok =False
        self.direita_ok =False

        self.result_condu_e = []
        self.result_condu_d = []
        self.result_iso_e = []
        self.result_iso_d = []

    def run(self):
        while self._running == True:
            # Emite o sinal para atualizar a interface do usuário
            QApplication.processEvents()  # Mantém a UI responsiva após iniciar as threads
            try:
                if self.operacao.em_execucao == True:
                    # Limpa todas as saídas
                    if self.operacao.rotina.abaixa_pistao() == True:
                        # self.operacao.rotina.limpa_saidas_esquerda_direita()# Desativa todos os relés por segurança
                        if self.operacao.habili_desbilita_esquerdo == True:
                            self.operacao.qual_teste = self.operacao.TESTE_COND_E
                            self.result_condu_e = self.operacao.rotina.esquerdo_direito_condutividade(0)# Testa O lado esquerdo
                            # Verifica condutividade
                            cond = all(c[2] != 0 for c in self.result_condu_e)   
                            if cond == True:
                                self.operacao.esquerda_condu_ok = 2 # Sinaliza para execução, que passou
                                # Se condutividade passou continua testando isolação
                                self.operacao.qual_teste = self.operacao.TESTE_ISO_E
                                self.result_iso_e = self.operacao.rotina.esquerdo_direito_isolacao(0)# Testa O lado esquerdo
                                # Verifica isolação
                                iso = all(i[2] != 1 for i in self.result_iso_e) 
                                if iso == True:
                                    self.operacao.esquerda_iso_ok = 2 # Sinaliza para execução, que passou
                                else:
                                    self.operacao.esquerda_iso_ok = 1 # Sinaliza para execução, que não passou
                                    self.operacao._visualiza_iso_e = True
                            else:
                                iso = False
                                self.result_iso_e = self.operacao.rotina.fake_isolacao_esquerdo()# Popula lista com valores falsos
                                self.operacao.esquerda_condu_ok = 1 # Sinaliza para execução, que não passou
                                self.operacao._visualiza_condu_e = True
                                self.operacao.esquerda_iso_ok = 1 # Sinaliza para execução, que não passou
                                self.operacao._visualiza_iso_e = True

                            # Se teste de condutividade e de isolação passaram
                            if cond == True and iso ==  True:
                                self.operacao.rotina.marca_peca_esquerda()
                                self.esquerda_ok = True
                            else:
                                self.esquerda_ok = False

                            # garante que todas os eletrodos fiquem verdes para ser tocados depois
                            # self.operacao._carrega_eletrodos(self.operacao.rotina.coord_eletrodo_esquerdo, "E")# O 'E' é para formar o texto que criará o objeto lbEletrodo1_E   
                        else:
                            self.esquerda_ok = True # Se Lado esquerdo não foi escolhido, sinaliza como ok para poder 
                                                    # continuar com o lado direito

                        if self.operacao.habili_desbilita_direito == True:
                            self.operacao.qual_teste = self.operacao.TESTE_COND_D
                            self.result_condu_d = self.operacao.rotina.esquerdo_direito_condutividade(1)# Testa O lado direito
                            # Verifica condutividade
                            cond = all(c[2] != 0 for c in self.result_condu_d)  
                            if cond == True:
                                self.operacao.direita_condu_ok = 2 # Sinaliza para execução, que passou
                                # Se condutividade passou continua testando isolação
                                self.operacao.qual_teste = self.operacao.TESTE_ISO_D
                                self.result_iso_d = self.operacao.rotina.esquerdo_direito_isolacao(1)# Testa O lado direito
                                # Verifica isolação
                                iso = all(i[2] != 1 for i in self.result_iso_d)
                                if iso == True:
                                    self.operacao.direita_iso_ok = 2 # Sinaliza para execução, que passou
                                else:
                                    self.operacao.direita_iso_ok = 1 # Sinaliza para execução, que não passou
                                    self.operacao._visualiza_iso_d = True
                            else:
                                iso = False
                                self.result_iso_d = self.operacao.rotina.fake_isolacao_direito()# Popula lista com valores falsos
                                self.operacao.direita_condu_ok = 1 # Sinaliza para execução, que não passou
                                self.operacao._visualiza_condu_d = True
                                self.operacao.direita_iso_ok = 1 # Sinaliza para execução, que não passou
                                self.operacao._visualiza_iso_d = True

                            # Se teste de condutividade e de isolação passaram
                            if cond == True and iso ==  True:
                                self.operacao.rotina.marca_peca_direita()
                                self.direita_ok = True
                            else:
                                self.direita_ok = False
                            # garante que todas os eletrodos fiquem verdes para ser tocados depois
                            # self.operacao._carrega_eletrodos(self.operacao.rotina.coord_eletrodo_direito, "D")# O 'D' é para formar o texto que criará o objeto lbEletrodo1_D
                        else:
                            self.direita_ok = True # Se Lado direito não foi escolhido, sinaliza como ok para poder 
                                                    # continuar com o lado esquerdo    
                            
                    if self.esquerda_ok == True and self.direita_ok == True:
                        self.operacao.rotina.acende_verde()
                        self.operacao.rotina.sobe_pistao()
                    else:
                        self.operacao.rotina.acende_vermelho()# Se acender vermelho, continua com pistão em baixo
                    
                    
                    # self.operacao.qual_teste = self.operacao.SEM_TESTE
                    # self.operacao.indica_cor_teste_condu("lbContinuIndicaE",self.operacao.CINZA, 0)
                    # self.operacao.indica_cor_teste_condu("lbContinuIndicaD",self.operacao.CINZA, 1)
                    # self.operacao.indica_cor_teste_iso("lbIsolaIndicaE",self.operacao.CINZA, 0)
                    # self.operacao.indica_cor_teste_iso("lbIsolaIndicaD",self.operacao.CINZA, 1)

                    # Emite o evento para conclusão so processo
                    self.sinal_execucao.emit(self.result_condu_e,self.result_iso_e,self.result_condu_d,self.result_iso_d)
                    # self.parar()
                    
                self.msleep(100)  # Cria um atraso de 100 mili segundo
                # print("ExecutaThread")
            except Exception as e:
                    logging.error(f"Erro na thread ExecutaRotinaThread: {e}")
                    self.parar()

            self.msleep(100)

    def iniciar(self):
        self._running = True
        self.start()
    def parar(self):
        self._running = False


class TelaExecucao(QDialog):
    def __init__(self, dado=None, io=None, db=None, rotina=None, nome_receita=None, nome_ordem_producao_esquerdo=None, nome_ordem_producao_direito=None, id_esquerdo=None, id_direito=None):
        super().__init__()
        try:
            self.inicializa_variaveis(dado, io, db, rotina, nome_receita, nome_ordem_producao_esquerdo, nome_ordem_producao_direito, id_esquerdo, id_direito)
            self.inicializa_estados()
            self.inicializa_cores()
            self.inicializa_contadores()
            self.inicializa_testes()
            self.inicializa_ui()
            self.inicializa_conexoes()
            self.carregar_configuracoes()
            self.inicializa_threads()
        except Exception as e:
            logging.error(f"Erro na inicialização da TelaExecucao: {e}")


    def inicializa_variaveis(self, dado, io, db, rotina, nome_receita, nome_ordem_producao_esquerdo, nome_ordem_producao_direito, id_esquerdo, id_direito):
        self.dado = dado
        self.io = io
        self.database = db
        self.rotina = rotina
        self.nome_receita = nome_receita
        self.tempo_ciclo = 0
        self._translate = QCoreApplication.translate
        self.nome_ordem_producao_esquerdo = nome_ordem_producao_esquerdo
        self.nome_ordem_producao_direito = nome_ordem_producao_direito
        self.id_esquerdo = id_esquerdo
        self.id_direito = id_direito

    def inicializa_estados(self):
        self.habili_desbilita_esquerdo = True
        self.habili_desbilita_direito = True
        self.execucao_habilita_desabilita = False
        self.em_execucao = False
        self._nao_passsou_peca_esquerdo = False
        self._nao_passsou_peca_direito = False
        self.esquerda_condu_ok = 0
        self.esquerda_iso_ok = 0
        self.direita_condu_ok = 0
        self.direita_iso_ok = 0
        self.id_rotina = None
        self.nome_op_esquerdo = None
        self.nome_op_direito = None
        self.quantidade_produzir_esquerdo = 0
        self.quantidade_produzir_direito = 0
        self.quantidade_produzida_esquerdo = 0
        self.quantidade_produzida_direito = 0

    def inicializa_cores(self):
        self.VERDE = "170, 255, 127"
        self.CINZA = "171, 171, 171"
        self.VERMELHO = "255, 0, 0"
        self.AZUL = "0,255,255"
        self.LILAZ = "192, 82, 206"

    def inicializa_contadores(self):
        self._cnt_peca_passou_e = 0
        self._cnt_peca_passou_d = 0
        self._cnt_peca_reprovou_e = 0
        self._cnt_peca_reprovou_d = 0
        self._cnt_peca_retrabalho_e = 0
        self._cnt_peca_retrabalho_d = 0
        self._cnt_pagina_erro = 0
        self._cnt_acionamento_botao = 0

    def inicializa_testes(self):
        self.SEM_TESTE = 0
        self.TESTE_COND_E = 1
        self.TESTE_COND_D = 2
        self.TESTE_ISO_E = 3
        self.TESTE_ISO_D = 4
        self.qual_teste = self.SEM_TESTE
        self._ofset_temo = 0
        self._retrabalho_esquerdo = False
        self._retrabalho_direito = False
        self.rotina_iniciada = False
        self._visualiza_condu_e = False
        self._visualiza_condu_d = False
        self._visualiza_iso_e = False
        self._visualiza_iso_d = False
        self.oscila_cor = False
        self.cond_e = []
        self.iso_e = []
        self.cond_d = []
        self.iso_d = []

    def inicializa_ui(self):
        self.msg = SimpleMessageBox()
        self.msg_box = MessageBox()
        self.ui = Ui_TelaExecucao()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowState.WindowMaximized)
        if self.dado.full_scream:
            self.setWindowState(Qt.WindowState.WindowFullScreen)

    def inicializa_conexoes(self):
        self.ui.btIniciar.clicked.connect(self.inicia_execucao)
        self.ui.btPausar.clicked.connect(self.pausa_execucao)
        self.ui.btFinalizar.clicked.connect(self.para_execucao)
        self.ui.btRetrabalharEsquerdo.clicked.connect(self.botao_retrabalho_esquerdo)
        self.ui.btRetrabalharDireito.clicked.connect(self.botao_retrabalho_direito)
        self.ui.btDescartarEsquerdo.clicked.connect(self.botao_descarte_esquerdo)
        self.ui.btDescartarDireito.clicked.connect(self.botao_descarte_direito)
        self.ui.lbImgEsquerdo.mousePressEvent = self.img_esquerda_clicada
        self.ui.lbImgDireito.mousePressEvent = self.img_direita_clicada
        self.ui.lbContinuIndicaE.mousePressEvent = self.select_visu_cond_e
        self.ui.lbContinuIndicaD.mousePressEvent = self.select_visu_cond_d
        self.ui.lbIsolaIndicaE.mousePressEvent = self.select_visu_iso_e
        self.ui.lbIsolaIndicaD.mousePressEvent = self.select_visu_iso_d

        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_C:
                self.dado.passa_condutividade = 1 if self.dado.passa_condutividade == 0 else 0
            elif event.key() == Qt.Key_I:
                self.dado.passa_isolacao = 1 if self.dado.passa_isolacao == 0 else 0
        return super(TelaExecucao, self).eventFilter(source, event)

    def carregar_configuracoes(self):
        self.load_config()

    def inicializa_threads(self):
        try:
            # ExecutaRotinaThread
            self.execucao_ = ExecutaRotinaThread(self)
            self.execucao_.sinal_execucao.connect(self.thread_execucao)
            self.execucao_.iniciar()

            # Atualizador Thread
            self.atualizador = Atualizador(self)
            self.atualizador.sinal_atualizar.connect(self.thread_atualizar_valor)
            self.atualizador.iniciar()

            QApplication.processEvents()  # Mantém a UI responsiva após iniciar as threads
        except Exception as e:
            logging.error(f"Erro na inicialização das threads: {e}")

    def load_config(self):
        self.qual_teste = self.SEM_TESTE
        self.muda_cor_obj("lbContinuIndicaE",self.CINZA)
        self.muda_cor_obj("lbContinuIndicaD",self.CINZA)
        self.muda_cor_obj("lbIsolaIndicaE",self.CINZA)
        self.muda_cor_obj("lbIsolaIndicaD",self.CINZA)

        self.ui.btRetrabalharEsquerdo.setDisabled(True)
        self.ui.btRetrabalharDireito.setDisabled(True)
        self.ui.btDescartarEsquerdo.setDisabled(True)
        self.ui.btDescartarDireito.setDisabled(True)
        self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina parada</p></body></html>"))
        self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        try:
            self.id_rotina, self.rotina_nome_rotina, self.rotina.url_img_esquerdo, self.rotina.url_img_direito, self.rotina.coord_eletrodo_esquerdo, self.rotina.coord_eletrodo_direito, self.rotina.condutividade_esquerdo, self.rotina.condutividade_direito, self.rotina.isolacao_esquerdo, self.rotina.isolacao_direito = self.database.search_name_receita(self.nome_receita)
     
            # Carrega nomes da op em variáveis globais
            self.nome_op_esquerdo = self.database.get_record_op_by_id(self.id_esquerdo)[1] if self.id_esquerdo else None
            self.nome_op_direito = self.database.get_record_op_by_id(self.id_direito)[1] if self.id_direito else None
            # Carrega a quantidade de peças a serem produzidas do lado esquerdo e direito
            self.quantidade_produzir_esquerdo = self.database.get_record_op_by_id(self.id_esquerdo)[2] if self.id_esquerdo else 0
            self.quantidade_produzir_direito = self.database.get_record_op_by_id(self.id_direito)[2] if self.id_direito else 0

            if self.nome_op_esquerdo == None:
                self.habili_desbilita_esquerdo = False
            if self.nome_op_direito == None:
                self.habili_desbilita_direito = False

            # Habilita ou desabilita as imagens
            self.ui.lbImgEsquerdo.setEnabled(self.habili_desbilita_esquerdo)
            self.ui.lbImgDireito.setEnabled(self.habili_desbilita_direito)

            # Carrega a quantidade de peças produzidas do lado esquerdo e direito
            try:
                reg = self.database.get_records_registro_op_by_op_id(self.id_esquerdo)
                
                self._cnt_peca_passou_e = max(reg, key=lambda x: x[2])[2] if reg else 0
                self._cnt_peca_reprovou_e = max(reg, key=lambda x: x[3])[3] if reg else 0
                self._cnt_peca_retrabalho_e = max(reg, key=lambda x: x[4])[4] if reg else 0
    
                self.quantidade_produzida_esquerdo = self._cnt_peca_passou_e + self._cnt_peca_reprovou_e + self._cnt_peca_retrabalho_e
            except:
                self._cnt_peca_passou_e = 0
                self._cnt_peca_reprovou_e = 0
                self._cnt_peca_retrabalho_e = 0
                self.quantidade_produzida_esquerdo = 0

            try:
                reg = self.database.get_records_registro_op_by_op_id(self.id_direito)

                self._cnt_peca_passou_d = max(reg, key=lambda x: x[2])[2] if reg else 0
                self._cnt_peca_reprovou_d = max(reg, key=lambda x: x[3])[3] if reg else 0
                self._cnt_peca_retrabalho_d = max(reg, key=lambda x: x[4])[4] if reg else 0

                self.quantidade_produzida_direito = self._cnt_peca_passou_d + self._cnt_peca_reprovou_d + self._cnt_peca_retrabalho_d
            except:
                self._cnt_peca_passou_d = 0
                self._cnt_peca_reprovou_d = 0
                self._cnt_peca_retrabalho_d = 0
                self.quantidade_produzida_direito = 0

            # Carrega as duas imagens
            dir_open = OpenFile(dado=self.dado, io=self.io, db=self.database)
            dir_open.load_image_url(image_path=self.rotina.url_img_esquerdo , size_x=self.ui.lbImgEsquerdo.width() , size_y=self.ui.lbImgEsquerdo.height())
            if dir_open.image != None:
                self.ui.lbImgEsquerdo.setPixmap(dir_open.image)
            dir_open.load_image_url(image_path=self.rotina.url_img_direito , size_x=self.ui.lbImgDireito.width() , size_y=self.ui.lbImgDireito.height())
            if dir_open.image != None:
                self.ui.lbImgDireito.setPixmap(dir_open.image)

            #Atribui nome do programa
            self.ui.lbNomePrograma_Esquerdo.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{self.nome_op_esquerdo}</p></body></html>"))
            self.ui.lbNomePrograma_Direito.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{self.nome_op_direito}</p></body></html>"))
            self.ui.lbNomeRotina.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{self.rotina_nome_rotina}</p></body></html>"))

            self.atualiza_producao_label("E", self.quantidade_produzida_esquerdo, self.quantidade_produzir_esquerdo)
            self.atualiza_producao_label("D", self.quantidade_produzida_direito, self.quantidade_produzir_direito)

            self.muda_texto_obj("txAprovadoE", self._cnt_peca_passou_e)
            self.muda_texto_obj("txReprovadoE", self._cnt_peca_reprovou_e)
            self.muda_texto_obj("txRetrabalhoE", self._cnt_peca_retrabalho_e)
            self.muda_texto_obj("txAprovadoD", self._cnt_peca_passou_d)
            self.muda_texto_obj("txReprovadoD", self._cnt_peca_reprovou_d)
            self.muda_texto_obj("txRetrabalhoD", self._cnt_peca_retrabalho_d)

            #Limpa os eletrodos
            self.limpaeletrodo()
            self.rotina.limpa_saidas_esquerda_direita()# Desativa todos os relés por segurança

            self._carrega_eletrodos(self.rotina.coord_eletrodo_esquerdo, "E")# O 'E' é para formar o texto que criará o objeto lbEletrodo1_E
            self._carrega_eletrodos(self.rotina.coord_eletrodo_direito, "D")# O 'D' é para formar o texto que criará o objeto lbEletrodo1_D

        except:
            print("Erro de carregamento...")

    def atualiza_producao_label(self, lado, produzido, produzir):
        if lado == "E":
            self.ui.lbQtdPrducaoEsquerdo.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{ produzido } de { produzir }</p></body></html>"))
        elif lado == "D":
            self.ui.lbQtdPrducaoDireito.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{ produzido } de { produzir }</p></body></html>"))
    
    def muda_texto_obj(self, obj_str, text):
        obj_tom_conec = f"{obj_str}"
        cur_obj_tom_conec = getattr(self.ui, obj_tom_conec)
        # cur_obj_tom_conec.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">{}</p></body></html>".format(text)))
        cur_obj_tom_conec.setText(str(text))
        # fm = self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{text}</p></body></html>")
        cur_obj_tom_conec.setText(self._translate("TelaExecucao", f"{text}"))
    def muda_cor_obj(self, obj_str, cor):
    
        obj_tom_conec = f"{obj_str}"
        cur_obj_tom_conec = getattr(self.ui, obj_tom_conec)
        cur_obj_tom_conec.setStyleSheet(f"background-color: rgb({cor});")

    def thread_atualizar_valor(self, data_hora):
        try:
            QMetaObject.invokeMethod(self, "atualiza_valor", Qt.QueuedConnection, Q_ARG(str, data_hora))
        except Exception as e:
            logging.error(f"Erro na thread_atualizar_valor: {e}")

    @pyqtSlot(str)
    def atualiza_valor(self, data_hora):
        try:
            self.ui.lbDataHora.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">{data_hora}</p></body></html>"))

            if self.execucao_habilita_desabilita == True  and (self._nao_passsou_peca_esquerdo and self._nao_passsou_peca_direito) == False:
            # if self.execucao_habilita_desabilita == True and  self.io.io_rpi.bot_acio_e == 0 and self.io.io_rpi.bot_acio_d == 0 and (self._nao_passsou_peca_esquerdo and self._nao_passsou_peca_direito) == False:
                self.rotina.apaga_torre()
                if self._cnt_acionamento_botao < 1:
                    self.rotina.flag_erro_geral = False
                    self._nao_passsou_peca_esquerdo = False
                    self._nao_passsou_peca_direito = False
                    self.em_execucao = True
                    self.tempo_ciclo = 0
                    self.oscila_cor = False
                    self._carrega_eletrodos(self.rotina.coord_eletrodo_esquerdo, "E")# O 'E' é para formar o texto que criará o objeto lbEletrodo1_E
                    self._carrega_eletrodos(self.rotina.coord_eletrodo_direito, "D")# O 'D' é para formar o texto que criará o objeto lbEletrodo1_D
                    self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Testando</p></body></html>"))
                    self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
                    self._cnt_acionamento_botao+=1# Incrementa para não passar por aqui novamente

                    # Variáveis para armazenar condicão de condutividade e isolação dos lados esquerdo e direito colocados em condição de não está sendo avaliado
                    # 0 = indica que não está sendo avaliado
                    # 1 = indica que não passou
                    # 2 = indica que passou
                    self.esquerda_condu_ok = 0
                    self.esquerda_iso_ok = 0
                    self.direita_condu_ok = 0
                    self.direita_iso_ok = 0
                
            if self.em_execucao == True and self._nao_passsou_peca_esquerdo == False:# Se está em execução e peça esquerda passou

                if self.qual_teste == self.SEM_TESTE:
                    self.indica_cor_teste_condu("lbContinuIndicaE",self.CINZA, 0)
                    self.indica_cor_teste_iso("lbIsolaIndicaE",self.CINZA, 0)
                elif self.qual_teste == self.TESTE_COND_E:
                    self.indica_cor_teste_condu("lbContinuIndicaE",self.VERDE, 0)
                    self.indica_cor_teste_iso("lbIsolaIndicaE",self.CINZA, 0)
                elif self.qual_teste == self.TESTE_ISO_E:
                    self.indica_cor_teste_condu("lbContinuIndicaE",self.CINZA, 0)
                    self.indica_cor_teste_iso("lbIsolaIndicaE",self.VERDE, 0)
                
                self.cor_eletrodo_esquerdo_teste()
            if self.em_execucao == True and self._nao_passsou_peca_direito == False:# Se está em execução e peça direita passou

                if self.qual_teste == self.SEM_TESTE:
                    self.indica_cor_teste_condu("lbContinuIndicaD",self.CINZA, 1)
                    self.indica_cor_teste_iso("lbIsolaIndicaD",self.CINZA, 1)
                elif self.qual_teste == self.TESTE_COND_D:
                    self.indica_cor_teste_condu("lbContinuIndicaD",self.VERDE, 1)
                    self.indica_cor_teste_iso("lbIsolaIndicaD",self.CINZA, 1)
                elif self.qual_teste == self.TESTE_ISO_D:
                    self.indica_cor_teste_condu("lbContinuIndicaD",self.CINZA, 1)
                    self.indica_cor_teste_iso("lbIsolaIndicaD",self.VERDE, 1)

                self.cor_eletrodo_direito_teste()

            # A Thread AtualizaValor atualiza de x em x ms
            # para que a indicação de tempo atualiza de 1 em 1 s, aplica-se o algoritimo de resto = 0
            if self.em_execucao == True:
                self._ofset_temo += 1
                if (self._ofset_temo % 5) == 0:
                    self.tempo_ciclo += 1
                    self.ui.txTempoCiclos.setText(f"{self.tempo_ciclo} s")
                    self._ofset_temo = 0
            if self.em_execucao == False and self._nao_passsou_peca_esquerdo == True:# Se está em execução e peça esquerda não passou
                # Habilita botão de descarte ou retrabalho
                self.ui.btDescartarEsquerdo.setDisabled(False)
                self.ui.btRetrabalharEsquerdo.setDisabled(False)


                if self._visualiza_condu_e == False and self._visualiza_condu_d == False and self._visualiza_iso_e == False and self._visualiza_iso_d == False:
                    self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Erros - Tocar na Tela para visualizar</p></body></html>"))
                    self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERMELHO});")

                try:
                    if self._visualiza_condu_e == True:
                        if self._cnt_pagina_erro > len(self.cond_e)-1:
                            self._cnt_pagina_erro=0


                        if self.habili_desbilita_esquerdo == True and self.cond_e != []:
                            self._carrega_eletrodos_esquerdo(self.rotina.coord_eletrodo_esquerdo, self.rotina.condutividade_esquerdo[f"ligacao{self.cond_e[self._cnt_pagina_erro][0]}"][1][0] , -1)
                            self.muda_cor_obj(f"lbEletrodo{self.rotina.condutividade_esquerdo[f'ligacao{self.cond_e[self._cnt_pagina_erro][0]}'][1][0]}_E",self.VERMELHO)
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Condutor: {self.cond_e[self._cnt_pagina_erro][1]}</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERMELHO});")
                        else:
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Não há erros de condutividade nessa peça</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")

                    if self._visualiza_iso_e == True:
                        if self._cnt_pagina_erro > len(self.iso_e)-1:
                            self._cnt_pagina_erro=0

                        if self.habili_desbilita_esquerdo == True and self.iso_e != []:
                            self._carrega_eletrodos_esquerdo(self.rotina.coord_eletrodo_esquerdo,self.rotina.isolacao_esquerdo[f"ligacao{self.iso_e[self._cnt_pagina_erro][0]}"][3],self.rotina.isolacao_esquerdo[f"ligacao{self.iso_e[self._cnt_pagina_erro][0]}"][4])
                            self.muda_cor_obj(f"lbEletrodo{self.rotina.isolacao_esquerdo[f'ligacao{self.iso_e[self._cnt_pagina_erro][0]}'][3]}_E",self.VERMELHO)
                            self.muda_cor_obj(f"lbEletrodo{self.rotina.isolacao_esquerdo[f'ligacao{self.iso_e[self._cnt_pagina_erro][0]}'][4]}_E",self.VERMELHO)
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Condutor: {self.iso_e[self._cnt_pagina_erro][1]}</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERMELHO});")
                        else:
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Não há erros de isolação nessa peça</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")

                except:
                    print("ultrapassou indice de lista esquerdo")

            if self.em_execucao == False and self._nao_passsou_peca_direito == True:# Se está em execução e peça direita não passou
                # Habilita botão de descarte ou retrabalho
                self.ui.btDescartarDireito.setDisabled(False)
                self.ui.btRetrabalharDireito.setDisabled(False)

                if self._visualiza_condu_e == False and self._visualiza_condu_d == False and self._visualiza_iso_e == False and self._visualiza_iso_d == False:
                    self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Erros - Tocar na Tela para visualizar</p></body></html>"))
                    self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERMELHO});")
                
                try:
                    if self._visualiza_condu_d == True:
                        if self._cnt_pagina_erro > len(self.cond_d)-1:
                            self._cnt_pagina_erro=0

                        if self.habili_desbilita_direito == True and self.cond_d != []:
                            self._carrega_eletrodos_direito(self.rotina.coord_eletrodo_direito, self.rotina.condutividade_direito[f"ligacao{self.cond_d[self._cnt_pagina_erro][0]}"][1][0] , -1)
                            self.muda_cor_obj(f"lbEletrodo{self.rotina.condutividade_direito[f'ligacao{self.cond_d[self._cnt_pagina_erro][0]}'][1][0]}_D",self.VERMELHO)
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Condutor: {self.cond_d[self._cnt_pagina_erro][1]}</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERMELHO});")
                        else:
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Não há erros de condutividade nessa peça</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")

                    if self._visualiza_iso_d == True:
                        if self._cnt_pagina_erro > len(self.iso_d)-1:
                            self._cnt_pagina_erro=0

                        if self.habili_desbilita_direito == True and self.iso_d != []:
                            self._carrega_eletrodos_direito(self.rotina.coord_eletrodo_direito,self.rotina.isolacao_direito[f"ligacao{self.iso_d[self._cnt_pagina_erro][0]}"][3],self.rotina.isolacao_direito[f"ligacao{self.iso_d[self._cnt_pagina_erro][0]}"][4])
                            self.muda_cor_obj(f"lbEletrodo{self.rotina.isolacao_direito[f'ligacao{self.iso_d[self._cnt_pagina_erro][0]}'][3]}_D",self.VERMELHO)
                            self.muda_cor_obj(f"lbEletrodo{self.rotina.isolacao_direito[f'ligacao{self.iso_d[self._cnt_pagina_erro][0]}'][4]}_D",self.VERMELHO) 
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Condutor: {self.iso_d[self._cnt_pagina_erro][1]}</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERMELHO});")
                        else:
                            self.ui.lbAvisos.setText(self._translate("TelaExecucao", f"<html><head/><body><p align=\"center\">Não há erros de isolação nessa peça</p></body></html>"))
                            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
                except:
                    print("ultrapassou indice de lista direito")
        except Exception as e:
            logging.error(f"Erro na atualização de valores: {e}")

    def indica_cor_teste_condu(self, obj, cor, lado):
        if lado == 0: # Se for esquerdo
            # Se condições de teste, que é verificado em ExecutaRotinaThread, tiver algum erro, pinta de vermelho
            if self.esquerda_condu_ok == 1:
                self.muda_cor_obj(obj,self.VERMELHO)
            elif self.esquerda_condu_ok == 2:# Se estiver ok, pinta de verde
                self.muda_cor_obj(obj,self.VERDE)
            else:
                self.muda_cor_obj(obj,cor) # caso contrario pinta na cor requerida
        else:
            # Se condições de teste, que é verificado em ExecutaRotinaThread, tiver algum erro, pinta de vermelho
            if self.direita_condu_ok == 1:
                self.muda_cor_obj(obj,self.VERMELHO)
            elif self.direita_condu_ok == 2:# Se estiver ok, pinta de verde
                self.muda_cor_obj(obj,self.VERDE)
            else:
                self.muda_cor_obj(obj,cor) # caso contrario pinta na cor requerida
    def indica_cor_teste_iso(self, obj, cor, lado):
        if lado == 0: # Se for esquerdo
            # Se condições de teste, que é verificado em ExecutaRotinaThread, tiver algum erro, pinta de vermelho
            if self.esquerda_iso_ok == 1:
                self.muda_cor_obj(obj,self.VERMELHO)
            elif self.esquerda_iso_ok == 2:# Se estiver ok, pinta de verde
                self.muda_cor_obj(obj,self.VERDE)
            else:
                self.muda_cor_obj(obj,cor) # caso contrario pinta na cor requerida
        else:
            # Se condições de teste, que é verificado em ExecutaRotinaThread, tiver algum erro, pinta de vermelho
            if self.direita_iso_ok == 1:
                self.muda_cor_obj(obj,self.VERMELHO)
            elif self.direita_iso_ok == 2:# Se estiver ok, pinta de verde
                self.muda_cor_obj(obj,self.VERDE)
            else:
                self.muda_cor_obj(obj,cor) # caso contrario pinta na cor requerida
    
    def cor_eletrodo_esquerdo_teste(self):

        try:
            if self.qual_teste == self.TESTE_COND_E:
                if self.rotina.eletrodo_testando_condu_e[0] != 0:
                    self.muda_cor_obj(f"lbEletrodo{self.rotina.eletrodo_testando_condu_e[0]}_E",self.AZUL)
                    self._carrega_eletrodos_esquerdo(self.rotina.coord_eletrodo_esquerdo, self.rotina.eletrodo_testando_condu_e[0], -1)

            if self.qual_teste == self.TESTE_ISO_E:
                if self.rotina.eletrodo_testando_iso_e[0] != 0:
                    self.muda_cor_obj(f"lbEletrodo{self.rotina.eletrodo_testando_iso_e[0]}_E",self.LILAZ)
                    self.muda_cor_obj(f"lbEletrodo{self.rotina.eletrodo_testando_iso_e[1]}_E",self.LILAZ)
                    self._carrega_eletrodos_esquerdo(self.rotina.coord_eletrodo_esquerdo, self.rotina.eletrodo_testando_iso_e[0], self.rotina.eletrodo_testando_iso_e[1])
        except:
            print("Erro de combinação de eletrodos esquerdo")

    def cor_eletrodo_direito_teste(self):
        try:
            if self.qual_teste == self.TESTE_COND_D:
                if self.rotina.eletrodo_testando_condu_d[0] != 0:
                    self.muda_cor_obj(f"lbEletrodo{self.rotina.eletrodo_testando_condu_d[0]}_D",self.AZUL)
                    self._carrega_eletrodos_direito(self.rotina.coord_eletrodo_direito, self.rotina.eletrodo_testando_condu_d[0], -1)

            if self.qual_teste == self.TESTE_ISO_D:
                if self.rotina.eletrodo_testando_iso_d[0] != 0:
                    self.muda_cor_obj(f"lbEletrodo{self.rotina.eletrodo_testando_iso_d[0]}_D",self.LILAZ)
                    self.muda_cor_obj(f"lbEletrodo{self.rotina.eletrodo_testando_iso_d[1]}_D",self.LILAZ)
                    self._carrega_eletrodos_direito(self.rotina.coord_eletrodo_direito, self.rotina.eletrodo_testando_iso_d[0], self.rotina.eletrodo_testando_iso_d[1])

        except:
            print("Erro de combinação de eletrodos direito")

    # Método chamado quando finaliza a thread de execução
    def thread_execucao(self, cond_e, iso_e, cond_d, iso_d):
        try:
            QMetaObject.invokeMethod(self, "execucao", Qt.QueuedConnection, 
                                    Q_ARG(list, cond_e), Q_ARG(list, iso_e), 
                                    Q_ARG(list, cond_d), Q_ARG(list, iso_d))
        except Exception as e:  
            logging.error(f"Erro na thread_execucao: {e}")

    @pyqtSlot(list, list, list, list)
    def execucao(self,  cond_e_, iso_e_, cond_d_, iso_d_):
        try:
            if self.em_execucao == True:
                self.qual_teste = self.SEM_TESTE
                self.indica_cor_teste_condu("lbContinuIndicaE",self.CINZA, 0)
                self.indica_cor_teste_condu("lbContinuIndicaD",self.CINZA, 1)
                self.indica_cor_teste_iso("lbIsolaIndicaE",self.CINZA, 0)
                self.indica_cor_teste_iso("lbIsolaIndicaD",self.CINZA, 1)

                self.cond_e.clear()
                self.cond_d.clear()
                self.iso_e.clear()
                self.iso_d.clear()
                print(f"Condutividade esquerdo: {cond_e_}")
                print(f"Isolação esquerdo: {iso_e_}")
                print(f"Condutividade direito: {cond_d_}")
                print(f"Isolação direito: {iso_d_}")
                self.em_execucao = False
                
                # Verifica se peças passaram
                if self.habili_desbilita_direito == True and self.habili_desbilita_esquerdo == True:# Se ambos os lados estiverem habilitados
                    if cond_e_ != [] and iso_e_ != [] and cond_d_ != [] and iso_d_ != []:
                        if self._verifica_condutividade_isolacao(cond_e_, iso_e_) == (True,True) and self._verifica_condutividade_isolacao(cond_d_, iso_d_) == (True,True):
                            self._carrega_peca_passou(0)# passou os dois lados
                        else:# Verifica qual dos dois não passaram
                            if self._verifica_condutividade_isolacao(cond_e_, iso_e_) == (True,True):
                                self._carrega_peca_passou(1)# passou a esquerda habilitada
                            else:
                                # passa para as variáveis somente o que não passou 
                                for i in cond_e_:
                                    if i[2] == 0:
                                        self.cond_e.append(i)
                                for i in iso_e_:
                                    if i[2] == 1:
                                        self.iso_e.append(i)
                                self.final_testes_nao_passou()
                                self._nao_passsou_peca_esquerdo = True
                            if self._verifica_condutividade_isolacao(cond_d_, iso_d_) == (True,True):
                                self._carrega_peca_passou(2)# passou a direita habilitada
                            else:
                                # passa para as variáveis somente o que não passou 
                                for i in cond_d_:
                                    if i[2] == 0:
                                        self.cond_d.append(i)
                                for i in iso_d_:
                                    if i[2] == 1:
                                        self.iso_d.append(i)
                                self.final_testes_nao_passou()
                                self._nao_passsou_peca_direito = True

                elif self.habili_desbilita_direito == False and self.habili_desbilita_esquerdo == True:# Se só esquerdo estiver habilitado
                    if cond_e_ != [] and iso_e_ != []:
                        if self._verifica_condutividade_isolacao(cond_e_, iso_e_) == (True,True):
                            self._carrega_peca_passou(1)# passou só a esquerda habilitada
                        else:
                            # passa para as variáveis somente o que não passou 
                            for i in cond_e_:
                                if i[2] == 0:
                                    self.cond_e.append(i)
                            for i in iso_e_:
                                if i[2] == 1:
                                    self.iso_e.append(i)
                            self._nao_passsou_peca_esquerdo = True
                            self.final_testes_nao_passou()

                elif self.habili_desbilita_direito == True and self.habili_desbilita_esquerdo == False:# Se só direito estiver habilitado
                    if cond_d_ != [] and iso_d_ != []:
                        if self._verifica_condutividade_isolacao(cond_d_, iso_d_) == (True,True):
                            self._carrega_peca_passou(2)# passou só a direita habilitada
                        else:
                            # passa para as variáveis somente o que não passou
                            for i in cond_d_:
                                if i[2] == 0:
                                    self.cond_d.append(i)
                            for i in iso_d_:
                                if i[2] == 1:
                                    self.iso_d.append(i)
                            self._nao_passsou_peca_direito = True
                            self.final_testes_nao_passou()
            self._cnt_acionamento_botao=0
        except Exception as e:  
            logging.error(f"Erro na execução: {e}")

    # qual_passou = 0 : Passou as duas peças
    #               1 : Passou só a esquerda habilitada
    #               2 : Passou só a direita habilitada
    def _carrega_peca_passou(self, qual_passou):
            if qual_passou == 0: # Se passou as duas peças
                if self._retrabalho_esquerdo == False:# Se não for um retrabalho 
                    self._cnt_peca_passou_e += 1
                    self.ui.txAprovadoE.setText( self._translate("TelaExecucao", f"{self._cnt_peca_passou_e}"))
                if self._retrabalho_direito == False:
                    self._cnt_peca_passou_d += 1
                    self.ui.txAprovadoD.setText(self._translate("TelaExecucao", f"{self._cnt_peca_passou_d}"))

                if self._retrabalho_esquerdo == True:
                    self._retrabalho_esquerdo = False # Para a próxima vez não ser um retrabalho de novo
                    self._cnt_peca_retrabalho_e+=1
                    self.ui.txRetrabalhoE.setText( self._translate("TelaExecucao", f"{self._cnt_peca_retrabalho_e}"))

                if self._retrabalho_direito == True:
                    self._retrabalho_direito = False
                    self._cnt_peca_retrabalho_d+=1
                    self.ui.txRetrabalhoD.setText( self._translate("TelaExecucao", f"{self._cnt_peca_retrabalho_d}"))
   
                self.quantidade_produzida_esquerdo+=1
                self.quantidade_produzida_direito+=1
                self.atualiza_producao_label("E", self.quantidade_produzida_esquerdo, self.quantidade_produzir_esquerdo)
                self.atualiza_producao_label("D", self.quantidade_produzida_direito, self.quantidade_produzir_direito)

                self._carrega_eletrodos(self.rotina.coord_eletrodo_esquerdo, "E")
                self._carrega_eletrodos(self.rotina.coord_eletrodo_direito, "D")
                self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
                self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
                
            elif qual_passou == 1: # Se passou só a esquerda habilitada
                if self._retrabalho_esquerdo == False:# Se não for um retralho 
                    self._cnt_peca_passou_e += 1
                    self.ui.txAprovadoE.setText( self._translate("TelaExecucao", f"{self._cnt_peca_passou_e}"))
                else:
                    self._retrabalho_esquerdo = False # Para a próxima vez não ser um retrabalho de novo
                
                    self._cnt_peca_retrabalho_e+=1
                    self.ui.txRetrabalhoE.setText( self._translate("TelaExecucao", f"{self._cnt_peca_retrabalho_e}"))

                self.quantidade_produzida_esquerdo+=1
                self.atualiza_producao_label("E", self.quantidade_produzida_esquerdo, self.quantidade_produzir_esquerdo)

                self._carrega_eletrodos(self.rotina.coord_eletrodo_esquerdo, "E")
                self._carrega_eletrodos(self.rotina.coord_eletrodo_direito, "D")
                self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
                self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
            elif qual_passou == 2: # Se passou só a direita habilitada
                if self._retrabalho_direito == False:# Se não for um retralho 
                    self._cnt_peca_passou_d += 1
                    self.ui.txAprovadoD.setText(self._translate("TelaExecucao", f"{self._cnt_peca_passou_d}"))
                else:
                    self._retrabalho_direito = False # Para a próxima vez não ser um retrabalho de novo

                    self._cnt_peca_retrabalho_d+=1
                    self.ui.txRetrabalhoD.setText( self._translate("TelaExecucao", f"{self._cnt_peca_retrabalho_d}"))

                self.quantidade_produzida_direito+=1
                self.atualiza_producao_label("D", self.quantidade_produzida_direito, self.quantidade_produzir_direito)

                self._carrega_eletrodos(self.rotina.coord_eletrodo_esquerdo, "E")
                self._carrega_eletrodos(self.rotina.coord_eletrodo_direito, "D")
                self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
                self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")

            self.salva_rotina()# Atualiza dados no banco de dados


    def _verifica_condutividade_isolacao(self, condu, iso):
        ret_cond = False
        ret_iso = False
        try:
            for i in range(len(condu)):
                if condu[i][2] == 0:
                    ret_cond = False
                    break
                else:
                    ret_cond = True
            for i in range(len(iso)):
                if iso[i][2] == 1:
                    ret_iso = False
                    break
                else:
                    ret_iso = True
        except:
            print("Erro em _verifica_condutividade_isolacao...")
            ret_cond = False
            ret_iso = False
        return ret_cond, ret_iso

    def _carrega_eletrodos(self, coord, lado):
        try:
            for index in range(0,len(coord)):
                if coord[index] != None:
                    obj_tom_conec = f"lbEletrodo{index}_{lado}"
                    cur_obj_tom_conec = getattr(self.ui, obj_tom_conec)
                    cur_obj_tom_conec.move( coord[index][0] - cur_obj_tom_conec.width() // 2,coord[index][1] - cur_obj_tom_conec.height() // 2)
                    cur_obj_tom_conec.setVisible(True)
                    cur_obj_tom_conec.setStyleSheet(f"background-color: rgb({self.VERDE});")

        except:
            print("Erro de objeto do eletrodo")

    def _carrega_eletrodos_esquerdo(self, coord, exceto, exceto2):
        try:
            for index in range(0,len(coord)):
                if coord[index] != None and index != exceto and index != exceto2:
                    obj_tom_conec = f"lbEletrodo{index}_E"
                    cur_obj_tom_conec = getattr(self.ui, obj_tom_conec)
                    cur_obj_tom_conec.move( coord[index][0] - cur_obj_tom_conec.width() // 2,coord[index][1] - cur_obj_tom_conec.height() // 2)
                    cur_obj_tom_conec.setVisible(True)
                    cur_obj_tom_conec.setStyleSheet(f"background-color: rgb({self.VERDE});")

        except:
            print("Erro de objeto do eletrodo esquerdo")

    def _carrega_eletrodos_direito(self, coord, exceto, exceto2):
        try:
            for index in range(0,len(coord)):
                if coord[index] != None and index != exceto and index != exceto2:
                    obj_tom_conec = f"lbEletrodo{index}_D"
                    cur_obj_tom_conec = getattr(self.ui, obj_tom_conec)
                    cur_obj_tom_conec.move( coord[index][0] - cur_obj_tom_conec.width() // 2,coord[index][1] - cur_obj_tom_conec.height() // 2)
                    cur_obj_tom_conec.setVisible(True)
                    cur_obj_tom_conec.setStyleSheet(f"background-color: rgb({self.VERDE});")

        except:
            print("Erro de objeto do eletrodo direito")
    
    def limpaeletrodo(self):
        self.ui.lbEletrodo1_D.setVisible(False)
        self.ui.lbEletrodo1_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo2_D.setVisible(False)
        self.ui.lbEletrodo2_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo3_D.setVisible(False)
        self.ui.lbEletrodo3_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo4_D.setVisible(False)
        self.ui.lbEletrodo4_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo5_D.setVisible(False)
        self.ui.lbEletrodo5_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo6_D.setVisible(False)
        self.ui.lbEletrodo6_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo7_D.setVisible(False)
        self.ui.lbEletrodo7_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo8_D.setVisible(False)
        self.ui.lbEletrodo8_D.setParent(self.ui.lbImgDireito) # Seta label para acertar coordenadas

        self.ui.lbEletrodo1_E.setVisible(False)
        self.ui.lbEletrodo1_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo2_E.setVisible(False)
        self.ui.lbEletrodo2_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo3_E.setVisible(False)
        self.ui.lbEletrodo3_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo4_E.setVisible(False)
        self.ui.lbEletrodo4_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo5_E.setVisible(False)
        self.ui.lbEletrodo5_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo6_E.setVisible(False)
        self.ui.lbEletrodo6_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo7_E.setVisible(False)
        self.ui.lbEletrodo7_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

        self.ui.lbEletrodo8_E.setVisible(False)
        self.ui.lbEletrodo8_E.setParent(self.ui.lbImgEsquerdo) # Seta label para acertar coordenadas

    def inicia_execucao(self):
        botoes_liberado = self._verifica_botoes_liberados()
        if self.execucao_habilita_desabilita == False:
            self.rotina.sobe_pistao()
            if botoes_liberado == True:
                self.execucao_habilita_desabilita = True# Habilita para executar programa
                self._desabilita_botoes(False)
                self.ui.lbAvisos.setVisible(True)
                self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
                self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
                self._cnt_acionamento_botao=0

    def _verifica_botoes_liberados(self):
        if self.ui.btRetrabalharEsquerdo.isEnabled() == False and self.ui.btRetrabalharDireito.isEnabled() == False and self.ui.btDescartarEsquerdo.isEnabled() == False and self.ui.btDescartarDireito.isEnabled() == False:
            return True
        else:
            return False

    def final_testes_nao_passou(self):
        self.execucao_habilita_desabilita = False# desabilita para executar programa
        self.em_execucao = False
        self.rotina.flag_erro_geral = True
        # Habilita botões que não podem ser acionados durante programa
        self._desabilita_botoes(True)
        self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Parada</p></body></html>"))
        self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        self._cnt_acionamento_botao=0
        

    def pausa_execucao(self):
        self.execucao_habilita_desabilita = False# desabilita para executar programa
        self.em_execucao = False
        self.rotina.flag_erro_geral = True
        # Habilita botões que não podem ser acionados durante programa
        self._desabilita_botoes(True)
        self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Parada</p></body></html>"))
        self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        self._cnt_acionamento_botao=0

        motivo_pause = MotivoPausa( dado=self.dado, io=self.io,db=self.database, rotina=self.rotina)
        motivo_pause.exec_()
        self.salva_motivo_parada(motivo_pause.motivo_pausa)

    def para_execucao(self):
        self.msg_box.exec(msg="Deseja realmente encerar rotina?")
        if self.msg_box.yes_no == True:
            self._nao_passsou_peca_esquerdo = False# Flag de peça não passo habilitada para novo teste
            self._nao_passsou_peca_direito = False
            self._desabilita_botoes(False)
            self.ui.lbAvisos.setVisible(True)
            self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
            self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
            self._cnt_acionamento_botao=0
            self.ui.btDescartarEsquerdo.setDisabled(True)# Volta a desabilitar esse botão
            self.ui.btDescartarDireito.setDisabled(True)# Volta a desabilitar esse botão
            self.ui.btRetrabalharEsquerdo.setDisabled(True)# Volta a desabilitar esse botão
            self.ui.btRetrabalharDireito.setDisabled(True)# Volta a desabilitar esse botão
            self.ui.lbContinuIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
            self.ui.lbContinuIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
            self.ui.lbIsolaIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
            self.ui.lbIsolaIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
            self._visualiza_condu_e = False
            self._visualiza_condu_d = False
            self._visualiza_iso_e = False
            self._visualiza_iso_d = False
            self.rotina_iniciada = False
            self.close()

    def botao_retrabalho_esquerdo(self):
        self._nao_passsou_peca_esquerdo = False# Flag de peça não passo habilitada para novo teste
        self._desabilita_botoes(False)
        self.ui.lbAvisos.setVisible(True)
        # self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
        # self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        # self._cnt_acionamento_botao=0
        self.ui.btDescartarEsquerdo.setDisabled(True)# Volta a desabilitar esse botão
        self.ui.btRetrabalharEsquerdo.setDisabled(True)# Volta a desabilitar esse botão
        self.ui.lbContinuIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
        # self.ui.lbContinuIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self.ui.lbIsolaIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
        # self.ui.lbIsolaIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self._visualiza_condu_e = False
        # self._visualiza_condu_d = False
        self._visualiza_iso_e = False
        # self._visualiza_iso_d = False
        self._retrabalho_esquerdo = True

        # Variáveis para armazenar condicão de condutividade e isolação dos lados esquerdo e direito colocados em condição de não está sendo avaliado
        # 0 = indica que não está sendo avaliado
        # 1 = indica que não passou
        # 2 = indica que passou
        self.esquerda_condu_ok = 0
        self.esquerda_iso_ok = 0
        # self.direita_condu_ok = 0
        # self.direita_iso_ok = 0

        # if (self.cond_e != [] or self.iso_e != []) and (self.cond_d != [] or self.iso_d != []):# se os dois lados estiverem com problemas
        #     self.ui.lbImgEsquerdo.setEnabled(True)
        #     self.ui.lbImgDireito.setEnabled(True)
        # if self.cond_e != [] or self.iso_e != []:# Se só o lado esquerdo estiver com problemas
        #     self.ui.lbImgEsquerdo.setEnabled(True)
        #     self.ui.lbImgDireito.setEnabled(False)
        # elif self.cond_d != [] or self.iso_d != []:# Se só o lado direito estiver com problemas
        #     self.ui.lbImgEsquerdo.setEnabled(False)
        #     self.ui.lbImgDireito.setEnabled(True)

    def botao_retrabalho_direito(self):
        self._nao_passsou_peca_direito = False
        self._desabilita_botoes(False)
        # self.ui.lbAvisos.setVisible(True)
        # self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
        # self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        # self._cnt_acionamento_botao=0
        self.ui.btDescartarDireito.setDisabled(True)# Volta a desabilitar esse botão
        self.ui.btRetrabalharDireito.setDisabled(True)# Volta a desabilitar esse botão
        # self.ui.lbContinuIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self.ui.lbContinuIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
        # self.ui.lbIsolaIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self.ui.lbIsolaIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
        # self._visualiza_condu_e = False
        self._visualiza_condu_d = False
        # self._visualiza_iso_e = False
        self._visualiza_iso_d = False
        self._retrabalho_direito = True

        # Variáveis para armazenar condicão de condutividade e isolação dos lados esquerdo e direito colocados em condição de não está sendo avaliado
        # 0 = indica que não está sendo avaliado
        # 1 = indica que não passou
        # 2 = indica que passou
        # self.esquerda_condu_ok = 0
        # self.esquerda_iso_ok = 0
        self.direita_condu_ok = 0
        self.direita_iso_ok = 0

        # if (self.cond_e != [] or self.iso_e != []) and (self.cond_d != [] or self.iso_d != []):# se os dois lados estiverem com problemas
        #     self.ui.lbImgEsquerdo.setEnabled(True)
        #     self.ui.lbImgDireito.setEnabled(True)
        # elif self.cond_e != [] or self.iso_e != []:# Se só o lado esquerdo estiver com problemas
        #     self.ui.lbImgEsquerdo.setEnabled(True)
        #     self.ui.lbImgDireito.setEnabled(False)
        # if self.cond_d != [] or self.iso_d != []:# Se só o lado direito estiver com problemas
        #     self.ui.lbImgEsquerdo.setEnabled(False)
        #     self.ui.lbImgDireito.setEnabled(True)



    def botao_descarte_esquerdo(self):
        self._nao_passsou_peca_esquerdo = False# Flag de peça não passo habilitada para novo teste
        self._desabilita_botoes(False)
        self.ui.lbAvisos.setVisible(True)
        self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
        self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        self._cnt_acionamento_botao=0
        self.ui.btDescartarEsquerdo.setDisabled(True)# Volta a desabilitar esse botão
        self.ui.btRetrabalharEsquerdo.setDisabled(True)# Volta a desabilitar esse botão
        self.ui.lbContinuIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self.ui.lbIsolaIndicaE.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self._visualiza_condu_e = False
        self._visualiza_iso_e = False

        # Variáveis para armazenar condicão de condutividade e isolação dos lados esquerdo e direito colocados em condição de não está sendo avaliado
        # 0 = indica que não está sendo avaliado
        # 1 = indica que não passou
        # 2 = indica que passou
        self.esquerda_condu_ok = 0
        self.esquerda_iso_ok = 0

        if self.cond_e != [] or self.iso_e != []:# Se só o lado esquerdo estiver com problemas
            self._cnt_peca_reprovou_e+=1
            self.ui.txReprovadoE.setText(f"{self._cnt_peca_reprovou_e}")
            self.quantidade_produzida_esquerdo+=1
            self.atualiza_producao_label("E", self.quantidade_produzida_esquerdo, self.quantidade_produzir_esquerdo)
        self.salva_rotina_esquerdo()

    def botao_descarte_direito(self):
        self._nao_passsou_peca_direito = False
        self._desabilita_botoes(False)
        self.ui.lbAvisos.setVisible(True)
        self.ui.lbAvisos.setText(self._translate("TelaExecucao", "<html><head/><body><p align=\"center\">Máquina pronta</p></body></html>"))
        self.ui.lbAvisos.setStyleSheet(f"background-color: rgb({self.VERDE});")
        self._cnt_acionamento_botao=0
        self.ui.btDescartarDireito.setDisabled(True)
        self.ui.btRetrabalharDireito.setDisabled(True)
        self.ui.lbContinuIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self.ui.lbIsolaIndicaD.setStyleSheet(f"background-color: rgb({self.CINZA});")
        self._visualiza_condu_d = False
        self._visualiza_iso_d = False

        # Variáveis para armazenar condicão de condutividade e isolação dos lados esquerdo e direito colocados em condição de não está sendo avaliado
        # 0 = indica que não está sendo avaliado
        # 1 = indica que não passou
        # 2 = indica que passou
        self.direita_condu_ok = 0
        self.direita_iso_ok = 0

        if self.cond_d != [] or self.iso_d != []:# Se só o lado direito estiver com problemas
            self._cnt_peca_reprovou_d+=1
            self.ui.txReprovadoD.setText(f"{self._cnt_peca_reprovou_d}")
            self.quantidade_produzida_direito+=1
            self.atualiza_producao_label("D", self.quantidade_produzida_direito, self.quantidade_produzir_direito)
        self.salva_rotina_direito()

    def img_esquerda_clicada(self, event):
        self._cnt_pagina_erro+=1
    
    def img_direita_clicada(self, event):
        self._cnt_pagina_erro+=1

    def select_visu_cond_e(self, event):
        if self.habili_desbilita_esquerdo == True and self._nao_passsou_peca_esquerdo == True:
            self._visualiza_condu_e = True
            self._visualiza_condu_d = False
            self._visualiza_iso_e = False
            self._visualiza_iso_d = False
            self.selecao_visualisacao()


    def select_visu_iso_e(self, event):
        if self.habili_desbilita_esquerdo == True and self._nao_passsou_peca_esquerdo == True:
            self._visualiza_condu_e = False
            self._visualiza_condu_d = False
            self._visualiza_iso_e = True
            self._visualiza_iso_d = False
            self.selecao_visualisacao()

    def select_visu_cond_d(self, event):
        if self.habili_desbilita_direito == True and self._nao_passsou_peca_direito == True:
            self._visualiza_condu_e = False
            self._visualiza_condu_d = True
            self._visualiza_iso_e = False
            self._visualiza_iso_d = False
            self.selecao_visualisacao()

    def select_visu_iso_d(self, event):
        if self.habili_desbilita_direito == True and self._nao_passsou_peca_direito == True:
            self._visualiza_condu_e = False
            self._visualiza_condu_d = False
            self._visualiza_iso_e = False
            self._visualiza_iso_d = True
            self.selecao_visualisacao()
    def selecao_visualisacao(self):
        if self.esquerda_condu_ok == 2: # Se condutividade está ok
            self.ui.lbContinuIndicaE.setStyleSheet(f"background-color: rgb({self.VERDE});")
        elif self.esquerda_condu_ok == 1: # Se condutividade não está ok
            self.ui.lbContinuIndicaE.setStyleSheet(f"background-color: rgb({self.VERMELHO});")

        if self.direita_condu_ok == 2: # Se condutividade está ok
            self.ui.lbContinuIndicaD.setStyleSheet(f"background-color: rgb({self.VERDE});")
        elif self.direita_condu_ok == 1: # Se condutividade não está ok
            self.ui.lbContinuIndicaD.setStyleSheet(f"background-color: rgb({self.VERMELHO});")

        if self.esquerda_iso_ok == 2: # Se isolação estiver ok
            self.ui.lbIsolaIndicaE.setStyleSheet(f"background-color: rgb({self.VERDE});")
        elif self.esquerda_iso_ok == 1: # Se isolação não estiver ok
            self.ui.lbIsolaIndicaE.setStyleSheet(f"background-color: rgb({self.VERMELHO});")
                
        if self.direita_iso_ok == 2: # Se isolação está ok
            self.ui.lbIsolaIndicaD.setStyleSheet(f"background-color: rgb({self.VERDE});")
        elif self.direita_iso_ok == 1: # Se isolação não estiver ok
            self.ui.lbIsolaIndicaD.setStyleSheet(f"background-color: rgb({self.VERMELHO});")

    def _desabilita_botoes(self, hab_dasab):
        # Desabilita ou habilita botões que não podem ser acionados durante programa
        self.ui.btContato.setEnabled(hab_dasab)

    def salva_rotina(self):
        try:
            if self.habili_desbilita_esquerdo == True:
                self.database.create_record_registro_op(self.id_esquerdo, self._cnt_peca_passou_e, self._cnt_peca_reprovou_e, self._cnt_peca_retrabalho_e)
            if self.habili_desbilita_direito == True:
                self.database.create_record_registro_op(self.id_direito, self._cnt_peca_passou_d, self._cnt_peca_reprovou_d, self._cnt_peca_retrabalho_d)
        except Exception as e:
            logging.error(f"Erro ao salvar rotina: {e}")

        if self.habili_desbilita_esquerdo == True and self.habili_desbilita_direito == True:
            if (self.quantidade_produzida_esquerdo == self.quantidade_produzir_esquerdo) and (self.quantidade_produzida_direito == self.quantidade_produzir_direito):
                self.msg.exec(f"Os lados esquerdo e direito atingiram a quantidade de peças a serem produzidas.\nEsquerdo: produzidos {self.quantidade_produzida_esquerdo} de {self.quantidade_produzir_esquerdo}.\nDireito: produzidos {self.quantidade_produzida_direito} de {self.quantidade_produzir_direito}.")

    def salva_rotina_esquerdo(self):
        try:
            if self.habili_desbilita_esquerdo == True:
                self.database.create_record_registro_op(self.id_esquerdo, self._cnt_peca_passou_e, self._cnt_peca_reprovou_e, self._cnt_peca_retrabalho_e)
        except Exception as e:
            logging.error(f"Erro ao salvar rotina esquerdo: {e}")

        if self.habili_desbilita_esquerdo == True:
            if self.quantidade_produzida_esquerdo == self.quantidade_produzir_esquerdo:
                self.msg.exec(f"O lado esquerdo atingiu a quantidade de peças a serem produzidas.\nProduzidos {self.quantidade_produzida_esquerdo} de {self.quantidade_produzir_esquerdo}.")     

    def salva_rotina_direito(self):
        try:
            if self.habili_desbilita_direito == True:
                self.database.create_record_registro_op(self.id_direito, self._cnt_peca_passou_d, self._cnt_peca_reprovou_d, self._cnt_peca_retrabalho_d)
        except Exception as e:
            logging.error(f"Erro ao salvar rotina direito: {e}")

        if self.habili_desbilita_direito == True:
            if self.quantidade_produzida_direito == self.quantidade_produzir_direito:
                self.msg.exec(f"O lado direito atingiu a quantidade de peças a serem produzidas.\nProduzidos {self.quantidade_produzida_direito} de {self.quantidade_produzir_direito}.")

    def salva_motivo_parada(self, motivo):
        try:
            if self.habili_desbilita_esquerdo == True:
                self.database.create_record_motivo_parada(self.id_esquerdo, motivo)
            if self.habili_desbilita_direito == True:
                self.database.create_record_motivo_parada(self.id_direito, motivo)
        except Exception as e:
            logging.error(f"Erro ao salvar motivo de parada: {e}")

    def salva_motivo_finalizado(self):
        try:
            if self.habili_desbilita_esquerdo == True:
                self.database.create_record_motivo_finalizacao(self.id_esquerdo)
            if self.habili_desbilita_direito == True:
                self.database.create_record_motivo_finalizacao(self.id_direito)
        except Exception as e:
            logging.error(f"Erro ao salvar motivo de finalizado: {e}")

    def salva_troca_usuario(self):
        try:
            if self.habili_desbilita_esquerdo == True:
                self.database.create_record_troca_usuario(self.id_esquerdo)
            if self.habili_desbilita_direito == True:
                self.database.create_record_troca_usuario(self.id_direito)
        except Exception as e:
            logging.error(f"Erro ao salvar troca de usuário: {e}")

    def closeEvent(self, event):
        try:
            self.atualizador.parar()
            self.atualizador.wait()  # Aguarde a thread finalizar

            self.execucao_.parar()
            self.execucao_.wait()  # Aguarde a thread finalizar
        except Exception as e:
            print(f"Erro ao finalizar threads: {e}")
        event.accept()