import sqlite3
from datetime import datetime
import json
import logging

# Configuração do logging
logging.basicConfig(filename='database.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class DataBase:
    def __init__(self, database_name='database.db'):
        try:
            self.conn = sqlite3.connect(database_name)
            self.cursor = self.conn.cursor()

            self._login_default = "QUALIFIX" # Esse será o login master
            self._senha_default = "1420" # senha poderá ser mudado posteriormente
            self._permissao_default = 1 # 1 significa permissões de administrador

            self._login_user_default = "USUARIO" # Esse será o login master
            self._senha_user_default = "1234" # senha poderá ser mudado posteriormente
            self._permissao_user_default = 0 # 0 significa que não tem permissões de administrador

            self.create_table_login()
            self.create_table_receita()
            self.criar_tabela_op()
            self.criar_tabela_motivo_parada()
            self.criar_tabela_motivo_finalizacao()
            self.criar_tabela_troca_usuario()

            admin_temp = self.search_name_login(self._login_default)
            if admin_temp == None:
                data = [self._login_default, self._senha_default, self._permissao_default]
                self.create_record_login(data=data)
            user_temp = self.search_name_login(self._login_user_default)
            if user_temp == None:
                data = [self._login_user_default, self._senha_user_default, self._permissao_user_default]
                self.create_record_login(data=data)

        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ou inicializar o banco de dados: {e}")

    def create_table_login(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                                    id INTEGER PRIMARY KEY,
                                    usuario TEXT,
                                    senha TEXT,
                                    permissao INTEGER
                                    )''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela login: {e}")

    def create_table_receita(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS receita (
                    id INTEGER PRIMARY KEY,
                    nome_programa TEXT,
                    url_img_esquerdo TEXT,
                    url_img_direito TEXT,
                    coord_eletrodo_esquerdo TEXT,
                    coord_eletrodo_direito TEXT,
                    condutividade_esquerdo TEXT,
                    condutividade_direito TEXT,
                    isolacao_esquerdo TEXT,
                    isolacao_direito TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela receita: {e}")

    def criar_tabela_op(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS op (
                        id INTEGER PRIMARY KEY,
                        ordem_producao TEXT,
                        quantidade_produzir INTEGER,
                        receita_peca TEXT,
                        esquerda_direita TEXT,
                        login TEXT,
                        criado TIMESTAMP,
                        finalizado TIMESTAMP,
                        fim_op INTEGER
                        )''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela rotina: {e}")
    
    def criar_tabela_motivo_parada(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS motivo_parada (
                        id INTEGER PRIMARY KEY,
                        op_id INTEGER,
                        motivo TEXT,
                        FOREIGN KEY(op_id) REFERENCES op(id)
                        )''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela motivo_parada: {e}")

    def criar_tabela_motivo_finalizacao(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS motivo_finalizacao (
                        id INTEGER PRIMARY KEY,
                        op_id INTEGER,
                        motivo TEXT,
                        FOREIGN KEY(op_id) REFERENCES op(id)
                        )''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela motivo_finalizacao: {e}")

    def criar_tabela_troca_usuario(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS troca_usuario (
                        id INTEGER PRIMARY KEY,
                        op_id INTEGER,
                        usuario_antigo TEXT,
                        usuario_novo TEXT,
                        timestamp TIMESTAMP,
                        FOREIGN KEY(op_id) REFERENCES op(id)
                        )''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela troca_usuario: {e}")

    def create_record_motivo_parada(self, op_id, motivo):
        try:
            self.cursor.execute('''
                INSERT INTO motivo_parada (op_id, motivo)
                VALUES (?, ?)
            ''', (op_id, motivo))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar motivo_parada: {e}")

    def get_record_motivo_parada_by_id(self, record_id):
        try:
            self.cursor.execute('SELECT * FROM motivo_parada WHERE id = ?', (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar motivo_parada pelo ID: {e}")
            return None

    def get_records_motivo_parada_by_op_id(self, op_id):
        try:
            self.cursor.execute('SELECT * FROM motivo_parada WHERE op_id = ?', (op_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar registros de motivo_parada pelo op_id: {e}")
            return []

    def update_record_motivo_parada(self, record_id, motivo):
        try:
            self.cursor.execute('''
                UPDATE motivo_parada
                SET motivo = ?
                WHERE id = ?
            ''', (motivo, record_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar motivo_parada: {e}")

    def delete_record_motivo_parada(self, record_id):
        try:
            self.cursor.execute('DELETE FROM motivo_parada WHERE id = ?', (record_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar motivo_parada: {e}")

    def create_record_motivo_finalizacao(self, op_id, motivo):
        try:
            self.cursor.execute('''
                INSERT INTO motivo_finalizacao (op_id, motivo)
                VALUES (?, ?)
            ''', (op_id, motivo))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar motivo_finalizacao: {e}")

    def get_record_motivo_finalizacao_by_id(self, record_id):
        try:
            self.cursor.execute('SELECT * FROM motivo_finalizacao WHERE id = ?', (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar motivo_finalizacao pelo ID: {e}")
            return None

    def get_records_motivo_finalizacao_by_op_id(self, op_id):
        try:
            self.cursor.execute('SELECT * FROM motivo_finalizacao WHERE op_id = ?', (op_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar registros de motivo_finalizacao pelo op_id: {e}")
            return []

    def update_record_motivo_finalizacao(self, record_id, motivo):
        try:
            self.cursor.execute('''
                UPDATE motivo_finalizacao
                SET motivo = ?
                WHERE id = ?
            ''', (motivo, record_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar motivo_finalizacao: {e}")

    def delete_record_motivo_finalizacao(self, record_id):
        try:
            self.cursor.execute('DELETE FROM motivo_finalizacao WHERE id = ?', (record_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar motivo_finalizacao: {e}")

    def create_record_troca_usuario(self, op_id, usuario_antigo, usuario_novo, timestamp):
        try:
            self.cursor.execute('''
                INSERT INTO troca_usuario (op_id, usuario_antigo, usuario_novo, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (op_id, usuario_antigo, usuario_novo, timestamp))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar troca_usuario: {e}")

    def get_record_troca_usuario_by_id(self, record_id):
        try:
            self.cursor.execute('SELECT * FROM troca_usuario WHERE id = ?', (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar troca_usuario pelo ID: {e}")
            return None

    def get_records_troca_usuario_by_op_id(self, op_id):
        try:
            self.cursor.execute('SELECT * FROM troca_usuario WHERE op_id = ?', (op_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar registros de troca_usuario pelo op_id: {e}")
            return []

    def update_record_troca_usuario(self, record_id, usuario_antigo, usuario_novo, timestamp):
        try:
            self.cursor.execute('''
                UPDATE troca_usuario
                SET usuario_antigo = ?, usuario_novo = ?, timestamp = ?
                WHERE id = ?
            ''', (usuario_antigo, usuario_novo, timestamp, record_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar troca_usuario: {e}")

    def delete_record_troca_usuario(self, record_id):
        try:
            self.cursor.execute('DELETE FROM troca_usuario WHERE id = ?', (record_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar troca_usuario: {e}")
    
    def criar_tabela_registro_op(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS registro_op (
                        id INTEGER PRIMARY KEY,
                        op_id INTEGER,
                        peca_aprovada INTEGER,
                        peca_reprovada INTEGER,
                        peca_retrabalhada INTEGER,
                        FOREIGN KEY(op_id) REFERENCES op(id)
                        )''')
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar a tabela registro_op: {e}")

    def create_record_registro_op(self, op_id, peca_aprovada, peca_reprovada, peca_retrabalhada):
        try:
            self.cursor.execute('''
                INSERT INTO registro_op (op_id, peca_aprovada, peca_reprovada, peca_retrabalhada)
                VALUES (?, ?, ?, ?)
            ''', (op_id, peca_aprovada, peca_reprovada, peca_retrabalhada))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar registro_op: {e}")

    def get_record_registro_op_by_id(self, record_id):
        try:
            self.cursor.execute('SELECT * FROM registro_op WHERE id = ?', (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar registro_op pelo ID: {e}")
            return None

    def get_records_registro_op_by_op_id(self, op_id):
        try:
            self.cursor.execute('SELECT * FROM registro_op WHERE op_id = ?', (op_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar registros de registro_op pelo op_id: {e}")
            return []

    def update_record_registro_op(self, record_id, peca_aprovada, peca_reprovada, peca_retrabalhada):
        try:
            self.cursor.execute('''
                UPDATE registro_op
                SET peca_aprovada = ?, peca_reprovada = ?, peca_retrabalhada = ?
                WHERE id = ?
            ''', (peca_aprovada, peca_reprovada, peca_retrabalhada, record_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar registro_op: {e}")

    def delete_record_registro_op(self, record_id):
        try:
            self.cursor.execute('DELETE FROM registro_op WHERE id = ?', (record_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar registro_op: {e}")

    def create_record_op(self, ordem_producao, quantidade_produzir, receita_peca, esquerda_direita, login, criado, finalizado, fim_op):
        try:
            self.cursor.execute('''
                INSERT INTO op (ordem_producao, quantidade_produzir, receita_peca, esquerda_direita, login, criado, finalizado, fim_op)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ordem_producao, quantidade_produzir, receita_peca, esquerda_direita, login, criado, finalizado, fim_op))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar op: {e}")

    def get_record_op_by_id(self, record_id):
        try:
            self.cursor.execute('SELECT * FROM op WHERE id = ?', (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar op pelo ID: {e}")
            return None

    def get_all_records_op(self):
        try:
            self.cursor.execute('SELECT * FROM op')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar todos os registros de op: {e}")
            return []
        
    def get_all_records_op_by_esquerdo_direito(self, esquerda_direita):
        try:
            self.cursor.execute('SELECT * FROM op WHERE esquerda_direita = ?', (esquerda_direita,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar todos os registros de op pelo lado: {e}")
            return []
    
    def get_all_records_op_by_ordem_producao_esquerdo_direito(self, ordem_producao, esquerda_direita):
        try:
            self.cursor.execute('SELECT * FROM op WHERE ordem_producao = ? AND esquerda_direita = ?', (ordem_producao, esquerda_direita))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar todos os registros de op pelo lado e ordem de produção: {e}")
            return []
        
    def record_op_exists(self, ordem_producao, esquerda_direita):
        try:
            self.cursor.execute('SELECT * FROM op WHERE ordem_producao = ? AND esquerda_direita = ?', (ordem_producao, esquerda_direita))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Erro ao verificar se a ordem de produção existe: {e}")
            return False
        
    def get_id_op(self, ordem_producao, esquerda_direita):
        try:
            self.cursor.execute('SELECT id FROM op WHERE ordem_producao = ? AND esquerda_direita = ?', (ordem_producao, esquerda_direita))
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar o ID da ordem de produção: {e}")
            return None

    def update_record_op(self, record_id, ordem_producao, quantidade_produzir, receita_peca, esquerda_direita, login, criado, finalizado, fim_op):
        try:
            self.cursor.execute('''
                UPDATE op
                SET ordem_producao = ?, quantidade_produzir = ?, receita_peca = ?, esquerda_direita = ?, login = ?, criado = ?, finalizado = ?, fim_op = ?
                WHERE id = ?
            ''', (ordem_producao, quantidade_produzir, receita_peca, esquerda_direita, login, criado, finalizado, fim_op, record_id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar op: {e}")

    def delete_record_op(self, record_id):
        try:
            self.cursor.execute('DELETE FROM op WHERE id = ?', (record_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar op: {e}")


    def create_record_login(self, data):
        try:
            self.cursor.execute('''INSERT INTO login 
                                   (usuario, senha, permissao) 
                                   VALUES (?, ?, ?)''', data)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar registro login: {e}")

    def create_record_receita(self, nome_programa, url_img_esquerdo, url_img_direito,
                            coord_eletrodo_esquerdo, coord_eletrodo_direito,
                            condutividade_esquerdo, condutividade_direito,
                            isolacao_esquerdo, isolacao_direito):
        try:
            self.cursor.execute('''
                INSERT INTO receita (nome_programa, url_img_esquerdo, url_img_direito,
                                coord_eletrodo_esquerdo, coord_eletrodo_direito,
                                condutividade_esquerdo, condutividade_direito,
                                isolacao_esquerdo, isolacao_direito)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome_programa, url_img_esquerdo, url_img_direito,
                json.dumps(coord_eletrodo_esquerdo), json.dumps(coord_eletrodo_direito),
                json.dumps(condutividade_esquerdo), json.dumps(condutividade_direito),
                json.dumps(isolacao_esquerdo), json.dumps(isolacao_direito)))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar registro receita: {e}")

    def update_record_login(self, record_id, data):
        try:
            query = '''UPDATE login SET 
                       usuario=?, senha=?, permissao=?
                       WHERE id=?'''
            self.cursor.execute(query, data + [record_id])
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar registro login: {e}")

    def update_record_receita(self, id, nome_programa, url_img_esquerdo, url_img_direito,
                            coord_eletrodo_esquerdo, coord_eletrodo_direito,
                            condutividade_esquerdo, condutividade_direito,
                            isolacao_esquerdo, isolacao_direito):
        try:
            self.cursor.execute('''
                UPDATE receita SET nome_programa = ?, url_img_esquerdo = ?, url_img_direito = ?,
                                coord_eletrodo_esquerdo = ?, coord_eletrodo_direito = ?,
                                condutividade_esquerdo = ?, condutividade_direito = ?,
                                isolacao_esquerdo = ?, isolacao_direito = ?
                WHERE id = ?
            ''', (nome_programa, url_img_esquerdo, url_img_direito,
                json.dumps(coord_eletrodo_esquerdo), json.dumps(coord_eletrodo_direito),
                json.dumps(condutividade_esquerdo), json.dumps(condutividade_direito),
                json.dumps(isolacao_esquerdo), json.dumps(isolacao_direito),
                id))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao atualizar registro receita: {e}")

    def delete_record_login(self, record_id):
        try:
            query = 'DELETE FROM login WHERE id=?'
            self.cursor.execute(query, (record_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar registro login: {e}")

    def delete_login_name(self, name):
        try:
            query = 'DELETE FROM login WHERE usuario=?'
            self.cursor.execute(query, (name,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar login pelo nome: {e}")

    def delete_receita_name(self, nome_programa):
        try:
            self.cursor.execute('DELETE FROM receita WHERE nome_programa = ?', (nome_programa,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar receita pelo nome: {e}")

    def delete_receita_id(self, id):
        try:
            self.cursor.execute('DELETE FROM receita WHERE id = ?', (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Erro ao deletar receita pelo ID: {e}")

    def search_record_login(self, record_id):
        try:
            query = 'SELECT * FROM login WHERE id=?'
            self.cursor.execute(query, (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar registro login pelo ID: {e}")
            return None

    def search_name_login(self, name):
        try:
            query = 'SELECT * FROM login WHERE usuario=?'
            self.cursor.execute(query, (name,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar login pelo nome: {e}")
            return None

    def search_name_receita(self, name):
        try:
            self.cursor.execute('SELECT * FROM receita WHERE nome_programa = ?', (name,))
            registro = self.cursor.fetchone()
            if registro:
                id, nome_programa, url_img_esquerdo, url_img_direito, \
                coord_eletrodo_esquerdo_json, coord_eletrodo_direito_json, \
                condutividade_esquerdo_json, condutividade_direito_json, \
                isolacao_esquerdo_json, isolacao_direito_json = registro
                
                # Converter JSON para dicionários
                coord_eletrodo_esquerdo = json.loads(coord_eletrodo_esquerdo_json)
                coord_eletrodo_direito = json.loads(coord_eletrodo_direito_json)
                condutividade_esquerdo = json.loads(condutividade_esquerdo_json)
                condutividade_direito = json.loads(condutividade_direito_json)
                isolacao_esquerdo = json.loads(isolacao_esquerdo_json)
                isolacao_direito = json.loads(isolacao_direito_json)
                
                return (id, nome_programa, url_img_esquerdo, url_img_direito,
                        coord_eletrodo_esquerdo, coord_eletrodo_direito,
                        condutividade_esquerdo, condutividade_direito,
                        isolacao_esquerdo, isolacao_direito)
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar receita pelo nome: {e}")
            return None

    def get_all_records_login(self):
        try:
            query = 'SELECT * FROM login'
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar todos os registros de login: {e}")
            return []

    def get_all_records_receita(self):
        try:
            self.cursor.execute('SELECT * FROM receita')
            registros = self.cursor.fetchall()
            return registros
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar todos os registros de receita: {e}")
            return []

    def stop(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logging.error(f"Erro ao fechar a conexão com o banco de dados: {e}")

    def __del__(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logging.error(f"Erro ao fechar a conexão com o banco de dados no __del__: {e}")

if __name__ == "__main__":
    db = DataBase()
