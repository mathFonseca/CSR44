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
import time
import random
import pickle
import pandas as pd
import socket
from pyDes import *

# Variaveis

ipHOST = '127.0.0.1'
PORT = 65230
KTGS = 'B7HA8172'

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

def getServiceKey(ID_Service):
    data = pd.read_csv("TGSDatabase.csv", index_col="serviceName")
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
                        # Data received is M3, from client.py
                        # [{ID_C + ID_S + T_R + N2 }K_c_tgs + T_c_tgs]
                        M3 = pickle.loads(data)
                        ktgs = KTGS
                        kc_tgs = decryptDES(M3[1][2],ktgs).decode()
                        ID_C = decryptDES(M3[1][0],ktgs).decode()
                        ID_S = decryptDES(M3[0][1],kc_tgs).decode()
                        T_R = decryptDES(M3[0][2],kc_tgs).decode()
                        N2 = decryptDES(M3[0][3],kc_tgs).decode()

                        # Build M4 
                        # [{K_c_s + T_A + N2}K_c_tgs + T_c_s]
                        # Onde T_c_s = {ID_C + T_A + K_c_s}K_s

                        kcs = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                        T_A = time.time() + int(T_R)*60
                        ks = getServiceKey(ID_S)

                        M4 = [[encryptDES(kcs,kc_tgs),encryptDES(str(T_A),kc_tgs),encryptDES(N2,kc_tgs)],[encryptDES(ID_C,ks),encryptDES(str(T_A),ks),encryptDES(kcs,ks)]]

                        M4data = pickle.dumps(M4)
                    conn.sendall(M4data)

if __name__ == "__main__":
    main()


