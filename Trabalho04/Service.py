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
PORT = 65130
KS = '27H741B4'

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
                        # Data received is M5, from client.py
                        M5 = pickle.loads(data)

                        # Build M6
                        answer = ''
                        kcs = decryptDES(M5[1][2],KS).decode()
                        ID_C = decryptDES(M5[0][0],kcs).decode()
                        S_R = decryptDES(M5[0][2],kcs).decode()
                        N3 = decryptDES(M5[0][3],kcs).decode()
                        T_A = decryptDES(M5[0][1],kcs).decode()

                        # Based on S_R, answer.
                        if(S_R == 'f'):
                            answer = " Hello " + str(ID_C) + "\n  z - Check Folders you can access. \n  x - Check Folders you cannot access. \nc - Exit\n"
                        elif(S_R == 'z'):
                            answer = " 01 - \ " + str(ID_C) + "\ " + "\n"
                            answer += " 02 - \group\common\ " + "\n"
                            answer += "\n\n"
                            answer += " That's all the folders you can access"
                            answer += "\n\n"
                            answer += " Hello " + str(ID_C) + "\n  z - Check Folders you can access. \n  x - Check Folders you cannot access. \nc - Exit\n"
                        elif(S_R == 'x'):
                            answer = " 01 - \admin\ " + "\n"
                            answer += " 02 - \group\private\ " + "\n"
                            answer += "\n\n"
                            answer += " 03 - Any other personal folder"
                            answer += "\n\n"
                            answer += " Hello " + str(ID_C) + "\n  z - Check Folders you can access. \n  x - Check Folders you cannot access. \nc - Exit\n"
                        elif(S_R == 'c'):
                            answer = '004'
                        else:
                            answer = 'ivalid input' + str(S_R) + '\n'
                            answer += " Hello " + str(ID_C) + "\n  z - Check Folders you can access. \n  x - Check Folders you cannot access. \nc - Exit\n"

                        if(time.time() > float(T_A)):
                            answer = '000'
                        
                        
                        M6 = [encryptDES(answer,kcs),encryptDES(N3,kcs)]
                        M6data = pickle.dumps(M6)
                    conn.sendall(M6data)







if __name__ == "__main__":
    main()