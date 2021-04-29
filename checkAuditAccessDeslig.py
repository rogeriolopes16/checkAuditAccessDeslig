import cx_Oracle
import mysql.connector
import json
import urllib3
import csv
from modules.getDataBase import *

urllib3.disable_warnings()
from datetime import datetime
datetime_format = "%d/%m/%Y - %H:%M:%S"

sysdate = datetime.now().strftime('%d/%m/%Y')
sysdateWSO2 = datetime.now().strftime('%m%Y')

print(str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S')+': Inicio da atividade'))

db = GetDataBase()

blazon = db.blazon('ACCOUNTS','0')
deslig_tabelao = db.oracle('FPW')
user_r12 = db.oracle('R12')
user_somar = db.oracle('SOMAR')

# --------------------------- Cria lista somente com CPF quem possui contas no Blazon ---------------------------
list_cpf_blazon = []
for list_cpf_user_blazon in blazon:
    list_cpf_blazon.append(list_cpf_user_blazon[4])


# --------------------------- Verificar do tablão quem tem conta ---------------------------
list_have_account = []
for checkAccountsTabelao in deslig_tabelao:
    if (checkAccountsTabelao[3] in list_cpf_blazon):
        list_have_account.append((checkAccountsTabelao[0],checkAccountsTabelao[1],checkAccountsTabelao[2],checkAccountsTabelao[3],checkAccountsTabelao[4],
                                  checkAccountsTabelao[5],checkAccountsTabelao[6],checkAccountsTabelao[7]))


# --------------------------- Cria nova lista com informações dos Recursos ---------------------------
list_account_resource = []
for checkAccountSystem in list_have_account:
    for checkAccountInBlazon in blazon:
        if (checkAccountSystem[3] == checkAccountInBlazon[4]):
            # fazendo select para encontrar data efetivação de rescisão
            blazon_efetiv_resc = db.blazon('EFETIVA1', str(checkAccountInBlazon[3]))
            max_date = max(int(blazon_efetiv_resc[0][0]), int(checkAccountSystem[7]))
            blazon_efetiv_resc = db.blazon('EFETIVA2', str(checkAccountInBlazon[3]))
            list_account_resource.append((checkAccountSystem[0],checkAccountSystem[1],checkAccountSystem[2],checkAccountSystem[3],checkAccountSystem[4],
                checkAccountSystem[5],checkAccountSystem[6],checkAccountInBlazon[2],checkAccountInBlazon[0],checkAccountInBlazon[3],blazon_efetiv_resc[0][0],max_date))

list_final = []
for ac_resource in list_account_resource:
    status = 'NÃO'
    if (ac_resource[7] in ('R12','R12 (APLICAÇÃO)')):
        for r12 in user_r12:
            if r12[0] == ac_resource[8]:
                if (ac_resource[11] < int(r12[4])):
                    status = 'SIM'
                list_final.append((ac_resource[0],ac_resource[1],ac_resource[2],ac_resource[3],ac_resource[4],ac_resource[5],ac_resource[6],ac_resource[7],ac_resource[8],
                                   ac_resource[9],ac_resource[10],r12[2],r12[3],status))

    elif (ac_resource[7] in ('SOMAR', 'SOMAR (APLICAÇÃO)')):
        for somar in user_somar:
            if somar[0] == ac_resource[8]:
                if (ac_resource[11] < int(somar[4])):
                    status = 'SIM'
                list_final.append((ac_resource[0],ac_resource[1],ac_resource[2],ac_resource[3],ac_resource[4],ac_resource[5],ac_resource[6],ac_resource[7],ac_resource[8],
                                   ac_resource[9],ac_resource[10],somar[2],somar[3],status))
    else:
        list_final.append((ac_resource[0], ac_resource[1], ac_resource[2], ac_resource[3],
                                   ac_resource[4], ac_resource[5], ac_resource[6], ac_resource[7],
                                   ac_resource[8], ac_resource[9], ac_resource[10], 'NÃO ENCONTRADO', 'NÃO ENCONTRADO', 'NÃO ENCONTRADO'))


contLinhas = 0
with open('C:/Automations/checkAuditAccessDeslig/reports/checkAuditAccessDeslig.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["EMPRESA", "MATRICULA", "NOME","CPF","ADMISSAO","RESCISAO","CARGO","RECURSO","CONTA","DATA_EFET_RESC","ULTIMO_LOGIN","DATA REVOGAÇÃO","ACESSO_POSTERIOR"])
    for result_list in list_final:
        writer.writerow([result_list[0], result_list[1], result_list[2], result_list[3], result_list[4], result_list[5], result_list[6], result_list[7]
                         , result_list[8], result_list[10], result_list[11], result_list[12], result_list[13]])
        contLinhas += 1

print('Quantidade de linhas no arquivo: '+ str(contLinhas))
print(str(datetime.now().strftime('%d/%m/%Y-%H:%M:%S')+': Fim da atividade'))