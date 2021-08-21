# ------------------------------
# Trabalho 4 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Kerberos
# ------------------------------

# ------------------------------
# Especificação: Usuário se conecta
# através do server AS 'AS', enviando a mensagem M1
# usando Tickets do Kerberos. Permissões são concedidadas
# para determinamos serviços em 'Services'  
# ------------------------------

# Bibliotecas
import string
import random
import pickle
import pandas as pd
import socket
from pyDes import *

# Variaveis

ipHOST = '127.0.0.1'
PORT = 65330
KTGS = 'B7HA8172'

def printMenu(menuType):
    print(menuType)

# Encrypt data with key using DES
def encryptDES(data, key):
    dataPrep = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    dataEncrypt = dataPrep.encrypt(data)
    return dataEncrypt

# Decrypt dataEncrypt with key using DES
def decryptDES(dataEncrypt, key):
    dataPrep = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    data = dataPrep.decrypt(dataEncrypt)
    return data

def getUserPassword(username):    
    data = pd.read_csv("ASDatabase.csv", index_col="username")
    return (data.loc[username][0])

def getTGSKey(ID_Service):
    data = pd.read_csv("ASTGSDatabase.csv", index_col="TGSName")
    return (data.loc[ID_Service][0])

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.bind((ipHOST,PORT))

        # Address the ipHost and Port to the socket, and keeps listening
        while True:
            soc.listen()
            # If hear something, accept the connection
            conn, addr = soc.accept()

            with conn:
                print("Connected in ",addr)
                # Once connected, reads the information
                connectionStatus = True
                while connectionStatus:
                    data = conn.recv(1024)
                    if(not data):
                        connectionStatus = False
                    else:
                        # Data received is M1, from client.py
                        print(" M1 received; ")
                        M1 = pickle.loads(data)
                        kc = getUserPassword(M1[0])[:8]
                        ID_S = decryptDES(M1[1][0], kc).decode()
                        T_R = decryptDES(M1[1][1],kc).decode()
                        N1 = decryptDES(M1[1][2],kc).decode()

                        # Builds M2{K_c_tgs + N_1}Kc + T_c_tgs]
                        # Onde T_c_tgs = {ID_C + T_R + K_c_tgs}K_tgs

                        kc_tgs = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        ktgs = getTGSKey(ID_S)
                        M2 = [[encryptDES(kc_tgs,kc),encryptDES(N1,kc)],
                        [encryptDES(M1[0],ktgs),encryptDES(T_R,ktgs),encryptDES(kc_tgs,ktgs) ]]

                        M2data = pickle.dumps(M2)
                        print(" M2 sent; ")
                    conn.sendall(M2data)

if __name__ == "__main__":
    main()