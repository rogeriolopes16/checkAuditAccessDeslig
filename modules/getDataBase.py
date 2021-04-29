import cx_Oracle
import mysql.connector
from settings.credentials import *
from settings.parameters import *
from settings.db import *

class GetDataBase:
    def __init__(self):
        pass

    def blazon(self, option, id):
        # --------------------------- Abrindo conexão com MYSql Blazon ---------------------------
        db = mysql.connector.connect(user=CRD_USER_DB_BLAZON, passwd=CRD_PWD_DB_BLAZON, host=PAR_BLAZON_IP, db=PAR_BLAZON_DB_NAME)
        cursor_blazon = db.cursor()
        if option == 'ACCOUNTS':
            cursor_blazon.execute(SELECT_USERS_ACTIVES_BLAZON)
        elif option == 'EFETIVA1':
            cursor_blazon.execute(SELECT_EFETIVA_RESCISAO1, (id,))
        elif option == 'EFETIVA2':
            cursor_blazon.execute(SELECT_EFETIVA_RESCISAO2, (id,))
        return cursor_blazon.fetchall()
        db.close()

    def oracle(self, option):
        if option == 'R12':
            user, pwd, tns, select = CRD_USER_DB_R12, CRD_PWD_DB_R12, PAR_R12_TNS, SELECT_ACCOUNTS_R12_SOMAR
        elif option == 'SOMAR':
            user, pwd, tns, select = CRD_USER_DB_SOMAR, CRD_PWD_DB_SOMAR, PAR_SOMAR_TNS, SELECT_ACCOUNTS_R12_SOMAR
        elif option == 'FPW':
            user, pwd, tns, select = CRD_USER_DB_FPW, CRD_PWD_DB_FPW, PAR_FPW_TNS, SELECT_DESLIGADOS_TABELAO

        conn_r = cx_Oracle.connect(user=user, password=pwd, dsn=tns)
        cr = conn_r.cursor()
        cr.execute(select)  # fazendo select de contas ativas no R12
        return cr.fetchall()
        cr.close()
