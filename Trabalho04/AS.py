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
import sys
import csv
import hashlib
import time
import pandas as pd
from pyDes import *

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

def main():
    # TODO: Connect to socket and listen for messages
    # TODO: Break Message 1 from Client.py and decrypt
    # TODO: Build Message 2 from TGS.py and send back

    while(not leaveFlag):
        printMenu(0)
        menuOption = input()

        # Account Creation. Log automatically if success
        if(menuOption == 'z' or menuOption == 'Z'):
            printMenu(1)
        # Log In. Moves to Service Interaction if success
        elif(menuOption == 'x' or menuOption == 'X'):
            printMenu(2)
        # Leave the software.
        elif(menuOption == 'c' or menuOption == 'C'):
            leaveFlag = True
            print("Thanks, have a great time!")
            sys.exit()     

if __name__ == "__main__":
    main()