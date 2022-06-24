from msilib.schema import Class
import sqlite3

from colorama import Cursor

from models import Tarefa, Usuario, Tipo, Status, Prioridade


# ------------------------------------------------------ SQL --------------------------------------------------------------------------------------

# Criação -----------------------------------------------------------------------------------------------------------------------------------------


SQL_CRIA_TAREFA = 'INSERT into TAREFA (NOME, DESCRICAO, TIPO_ID, STATUS_ID, PRIORIDADE_ID, USUARIO_ID) values (%s,%s , %s, %s, %s, %s)'

SQL_CRIA_USUARIO = 'INSERT into USUARIO (USERNAME, EMAIL, SENHA) values (%s, %s, %s)'

SQL_CRIA_TIPO = 'INSERT INTO TIPO (NOME, USUARIO_ID) VALUES (%s, %s)'

SQL_CRIA_STATUS = 'INSERT INTO STATUS (NOME) VALUES (%s)'

SQL_CRIA_PRIORIDADE = 'INSERT INTO PRIORIDADE (NOME) VALUES (%s)'


# Atualização -----------------------------------------------------------------------------------------------------------------------------------------


SQL_ATUALIZA_TAREFA = 'UPDATE TAREFA SET NOME = %s, DESCRICAO = %s, TIPO_ID = %s, STATUS_ID = %s, PRIORIDADE_ID = %s WHERE ID = %s'

SQL_ATUALIZA_USUARIO = 'UPDATE USUARIO SET USERNAME = %s, EMAIL = %s, SENHA = %s where ID = %s'

SQL_ATUALIZA_TIPO = 'UPDATE TIPO SET NOME = %s WHERE ID_TIPO = %s'

SQL_ATUALIZA_STATUS = 'UPDATE STATUS SET NOME = %s WHERE ID = %s'

SQL_ATUALIZA_PRIORIDADE = 'UPDATE PRIORIDADE SET NOME = %s WHERE ID = %s'


# Search -----------------------------------------------------------------------------------------------------------------------------------------


SQL_BUSCA_TAREFA = '''SELECT *, TIPO.NOME, TIPO.ID_STATUS, STATUS.NOME, STATUS.ID_STATUS, PRIORIDADE.NOME, PRIORIDADE.ID_PRIORIDADE
                      FROM TAREFA
                      INNER JOIN TIPO
                      ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                      INNER JOIN STATUS
                      ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                      INNER JOIN PRIORIDADE 
                      ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE'''
                      
SQL_BUSCA_TAREFA_NOME = '''SELECT *
                           FROM TAREFA
                           WHERE TAREFA.NOME
                           LIKE '%s'
                            '''

# BUSCA TAREFA POR USER -----------------------------------------------------------------------------------------------------------------------------------------


SQL_BUSCA_TAREFAS_DO_USUARIO = '''SELECT *, TIPO.NOME, TIPO.ID_TIPO, STATUS.NOME, STATUS.ID_STATUS, PRIORIDADE.NOME, PRIORIDADE.ID_PRIORIDADE
                                  FROM TAREFA
                                  INNER JOIN TIPO
                                  ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                                  INNER JOIN STATUS
                                  ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                                  INNER JOIN PRIORIDADE
                                  ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
                                  WHERE TAREFA.USUARIO_ID = %s'''

SQL_BUSCA_TIPO = 'SELECT * FROM TIPO'

SQL_BUSCA_STATUS = 'SELECT * FROM STATUS'

SQL_BUSCA_PRIORIDADE = 'SELECT * FROM PRIORIDADE'


# Search ID -----------------------------------------------------------------------------------------------------------------------------------------

SQL_BUSCA_TAREFA_POR_ID = '''SELECT *, TIPO.ID_TIPO, TIPO.NOME, STATUS.ID_STATUS, STATUS.NOME, PRIORIDADE.ID_PRIORIDADE, PRIORIDADE.NOME
                             FROM TAREFA
                             INNER JOIN TIPO
                             ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                             INNER JOIN STATUS
                             ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                             INNER JOIN PRIORIDADE
                             ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
                             WHERE TAREFA.ID = %s'''

SQL_BUSCA_TIPO_POR_ID= 'SELECT * FROM TIPO WHERE TIPO.TIPO_ID = %s'

SQL_BUSCA_TAREFA_POR_USUARIO = '''SELECT *, TIPO.ID_TIPO, TIPO.NOME, STATUS.ID_STATUS, STATUS.NOME, PRIORIDADE.ID_PRIORIDADE, PRIORIDADE.NOME
                                  FROM TAREFA
                                  INNER JOIN TIPO
                                  ON TAREFA.TIPO_ID = TIPO.ID_TIPO
                                  INNER JOIN STATUS
                                  ON TAREFA.STATUS_ID = STATUS.ID_STATUS
                                  INNER JOIN PRIORIDADE
                                  ON TAREFA.PRIORIDADE_ID = PRIORIDADE.ID_PRIORIDADE
                                  WHERE TAREFA.ID = %s AND USUARIO.ID = %s'''

SQL_USUARIO_POR_EMAIL = 'SELECT * FROM USUARIO WHERE EMAIL = %s'

SQL_BUSCA_USUARIO_POR_ID = 'SELECT * FROM USUARIO WHERE ID = %s'


# Delete -----------------------------------------------------------------------------------------------------------------------------------------


SQL_DELETA_TAREFA = 'DELETE FROM TAREFA WHERE ID = %s'

SQL_DELETA_TIPO = 'DELETE FROM TIPO WHERE ID_TIPO = %s'


# User Profile -----------------------------------------------------------------------------------------------------------------------------------------

SQL_CONTA_TAREFAS = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = %s'

SQL_CONTA_TAREFAS_FEITAS = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = %s AND TAREFA.STATUS_ID = 3'

SQL_CONTA_TAREFAS_FAZENDO = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = %s AND TAREFA.STATUS_ID = 2'

SQL_CONTA_TAREFAS_FAZER = 'SELECT COUNT(TAREFA.ID) FROM TAREFA WHERE TAREFA.USUARIO_ID = %s AND TAREFA.STATUS_ID = 1'

# -------------------- Trigger Try -----------------------------

SQL_DELETA_USER_ALL = '''DELIMITER //
                         CREATE TRIGGER deleteAll
                         AFTER DELETE ON USARIO
                         FOR EACH ROW
                         BEGIN
                         DELETE FROM TAREFA WHERE USUARIO_ID = OLD.ID
                         DELETE FROM TIPO WHERE USUARIO_ID = OLD.ID
                         END
                         //
                         DELIMITER ;'''


# ------------------- TAREFA -----------------------------------

class TarefaDao:
    def __init__(self, db) -> None:
        self.__db = db

    def salvar(self, tarefa):
        cur = self.__db.cur()

        if (tarefa._id):
            cur.execute(SQL_ATUALIZA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._id))

        else:
            cur.execute(SQL_CRIA_TAREFA, (tarefa._nome, tarefa._descricao, tarefa._tipo_id, tarefa._status_id, tarefa._prioridade_id, tarefa._usuario_id))
            
        self.__db.commit()
        
        return tarefa
    
    def listar(self):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TAREFA)
        tarefas = traduz_tarefas(cur.fetchall())
        return tarefas
    
    
    def listar_tarefas_por_usuario(self, usuario_id):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TAREFAS_DO_USUARIO, (usuario_id, ))
        tarefas = traduz_tarefas(cur.fetchall())
        
        return tarefas
    
    
    def busca_por_id(self, id):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TAREFA_POR_ID, (id, ))
        tupla = cur.fetchone()
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], id=tupla[0])
    
    
    def busca_por_usuario(self, id, usuario_id):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TAREFA_POR_USUARIO, (id, usuario_id))
        tupla = cur.fetchone()
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], id=tupla[0])
    
    
    def busca_por_nome(self, nome):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TAREFA_NOME, (nome, ))
        tarefas = traduz_tarefas(cur.fetchall())
        
        return tarefas
        
        
    def deletar(self, id):
        self.__db.cursor().execute(SQL_DELETA_TAREFA, (id, ))
        self.__db.commit()
    
    
def traduz_tarefas(tarefas):
    def cria_tarefas_com_tupla(tupla):
        return Tarefa(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], id=tupla[0])
    return list(map(cria_tarefas_com_tupla, tarefas))


# --------------------- TIPO -------------------------------

class TipoDao:
    def __init__(self, db):
        self.__db = db
        
    
    def salvar_tipo(self, tipo:Tipo):
        cur = self.__db.cursor()
        
        if (tipo._id):
            cur.execute(SQL_ATUALIZA_TIPO, (tipo._nome, tipo._usuario_id, tipo._id))
            
        else:
            cur.execute(SQL_CRIA_TIPO, (tipo._nome, tipo._usuario_id))
            tipo._id = cur.lastrowid
            
        self.__db.commit()
        
        return tipo
    
    
    def listar_tipos(self):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TIPO)
        tipo = traduz_tipo(cur.fetchall())
        return tipo

    def busca_por_id(self, id):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_TIPO_POR_ID, (id, ))
        tupla = cur.fetchone()
        return Tipo(tupla[1], tupla[2], id=tupla[0])

    def deletar_tipo(self, id):
        self.__db.cursor().execute(SQL_DELETA_TIPO, (id, ))
        self.__db.commit()
 

def traduz_tipo(tipo):
    def cria_tipo_com_tupla(tupla):
        return Tipo(tupla[1], tupla[2], tupla[0])
    return list(map(cria_tipo_com_tupla, tipo))

# --------------------- STATUS -----------------------------

class StatusDao:
    def __init__(self, db):
        self.__db = db
    
    
    def salvar_status(self, status):
        cur = self.__db.cursor()
        
        if (status._id):
            cur.execute(SQL_ATUALIZA_STATUS, (status._nome, status._id))
            
        else:
            cur.execute(SQL_CRIA_STATUS, [status._nome])
            status._id = cur.lastrowid
        
        self.__db.commit()
        
        return status
        
    
    def listar_status(self):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_STATUS)
        status = traduz_status(cur.fetchall())
        return status
    
    
def traduz_status(status):
    def cria_status_com_tupla(tupla):
        return Status(tupla[1], tupla[0])
    return list(map(cria_status_com_tupla, status))


# ------------------------------ PRIORIDADE -----------------------------------------------

class PrioridadeDao:
    def __init__(self, db):
        self.__db = db
        
    def salvar_prioridade(self, prioridade):
        cur = self.__db.cursor()
        
        if (prioridade._id):
            cur.exxecute(SQL_ATUALIZA_PRIORIDADE, (prioridade._nome, prioridade._id))
            
        else:
            cur.execute(SQL_CRIA_PRIORIDADE, [prioridade._nome])
            prioridade._id = cur.lastrowid
            
        self.__db.commit()
        
        return prioridade
    
    
    def listar_prioridades(self):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_PRIORIDADE)
        prioridade = traduz_prioridade(cur.fetchall())
        return prioridade
    
    
def traduz_prioridade(prioridade):
    def cria_prioridade_com_tupla(tupla):
        return Prioridade(tupla[1], tupla[0])
    return list(map(cria_prioridade_com_tupla, prioridade))
    

# --------------------- USUARIO -----------------------------------

class UsuarioDao:
    def __init__(self, db) -> None:
        self.__db = db
        
    def salvar_usuario(self, usuario):
        cur = self.__db.cursor()
        
        if (usuario._id):
            cur.execute(SQL_ATUALIZA_USUARIO, (usuario._nome, usuario._email, usuario._senha, usuario._id))
            
        else:
            cur.execute(SQL_CRIA_USUARIO, (usuario._nome, usuario._email, usuario._senha))
            
        self.__db.commit()
        return usuario

    def buscar_por_email_usu(self, email):
        cur =  self.__db.cursor()
        cur.execute(SQL_USUARIO_POR_EMAIL, (email,))
        dados = cur.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario
    
    
    def buscar_usuario_por_id(self, id):
        cur = self.__db.cursor()
        cur.execute(SQL_BUSCA_USUARIO_POR_ID, (id,))
        dados = cur.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario
    
    # Tentar otimizar o resultado
    def conta_tarefas(self, usuario_id):
        cur = self.__db.cursor()
        cur.execute(SQL_CONTA_TAREFAS, (usuario_id,))
        tarefas_qnt = cur.fetchone()
        if tarefas_qnt:
            return tarefas_qnt
        else:
            return 0
        
    
    def conta_tarefas_prontas(self, usuario_id):
        cur = self.__db.cursor()
        cur.execute(SQL_CONTA_TAREFAS_FEITAS, (usuario_id,))
        tarefas_prontas = cur.fetchone()
        if tarefas_prontas:
            return tarefas_prontas
        else:
            return 0
        
    
    def conta_tarefas_fazer(self, usuario_id):
        cur = self.__db.cursor()
        cur.execute(SQL_CONTA_TAREFAS_FAZER, (usuario_id,))
        tarefas_fazer = cur.fetchone()
        if tarefas_fazer:
            return tarefas_fazer
        else:
            return 0
        
    
    def conta_tarefas_fazendo(self, usuario_id):
        cur = self.__db.cursor()
        cur.execute(SQL_CONTA_TAREFAS_FAZENDO, (usuario_id,))
        tarefas_fazendo = cur.fetchone()
        if tarefas_fazendo:
            return tarefas_fazendo
        else:
            return 0
    
def traduz_usuario(tupla):
    return Usuario(tupla[1], tupla[2], tupla[3], id=tupla[0])