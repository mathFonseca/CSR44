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
import socket
import pickle
import secrets
import hashlib
import time
import pandas as pd
from pyDes import *

# Variaveis
ipHOST = '127.0.0.1'
ASPORT = 65330
TGSPORT = 65230
SPORT = 65130

# Print Section for User Interaction
def printMenu(menuType = 0, username = 'Default'):
    if(menuType == 0):
        print("------------------------------")
        print("====== Welcome!, please select options below: ======")
        print(" Z - Create Account")
        print(" X - Login")
        print(" C - Leave")
        print("====== Tip: The menu is not case sensitive ======")        
        print("------------------------------")
    
    if(menuType == 1):
        print("------------------------------")
        print("====== Create Account Menu ======")
        print("====== Tip: The credentials will be case sensitive ======")

    if(menuType == 2):
        print("------------------------------")
        print("====== Login Menu ======")
        print("====== Tip: The credentials will be case sensitive ======")
    
    if(menuType == 3):
        print("------------------------------")
        print("====== Welcome! " + str(username) + "======")

    if(menuType == 4):
        print("------------------------------")
        print("====== Welcome! " + str(username) + " , please select options below: ======")
        print(" Z - Service 1")
        print(" X - Service 2")
        print(" C - Leave")
        print("====== Tip: The menu is not case sensitive ======")        
        print("------------------------------")

    if(menuType == 6):
        print("------------------------------")
        print("====== Thanks for using our services! ======")

def login():
    # Step 1 - Print Menu
    printMenu(2)
    # User Input
    accountFlag = False
    resultFlag = -1
    while(not accountFlag):
        username = input("Username: ")
        password = input("Password: ")
        if(signIn(username, password)):
            accountFlag = True
            resultFlag = 1
        else:
            print("Wrond credentials, please try again!")
            accountFlag = False

    return resultFlag

# Verify if username is available
# Returns True if it's available, False if it's already in use
def verifyUsername(username):
    columnOrder = ["username","password"]
    data = pd.read_csv("userDatabase.csv", usecols=columnOrder)
    for user in data["username"]:
        if user == username:
            return False
    return True

# Verify user credentials
def signIn(username, password):
    userData = pd.read_csv("userDatabase.csv", index_col="username")

    if(not verifyUsername(username)):
        if(userData.loc[username][0] != password):
            return False
        else:
            return True
    return False

# Register new user on database
def signUp(username, password):
    with open('userDatabase.csv', 'a+', newline='') as userDatabase:
        newRow = csv.writer(userDatabase, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newRow.writerow([username, password])
    return

# Send userdata to AS database
def send2AS(username,password):
    with open('ASDatabase.csv', 'a+', newline='') as ASDatabase:
        newRow = csv.writer(ASDatabase, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newRow.writerow([username, password])
    return

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

    # Step 1 - User interaction
    leaveFlag = False
    userLogged = False

    while(not leaveFlag):
        printMenu(0)
        menuOption = input()

        # Account Creation. Log automatically if success
        if(menuOption == 'z' or menuOption == 'Z'):

            # Print Menu for Account Creation.
            printMenu(1)
            username = input("Username: ")
            if(verifyUsername(username)):
                password = input("Password: ")
                password = hashlib.sha256(password.encode()).hexdigest()

                signUp(username,password)
                send2AS(username,password)
                print(" Account created succesfully. Please Log In")
                time.sleep(5)

            else:
                print("Username already in use, try another one!")

        # Log In. Moves to Service Interaction if success
        elif(menuOption == 'x' or menuOption == 'X'):
            printMenu(2)
            username = input("Username: ")
            password = input("Password: ")

            password = hashlib.sha256(password.encode()).hexdigest()
            if(signIn(username,password)):
                printMenu(3,username)
                userLogged = True
                leaveFlag = True
            else:
                print("Sorry, wrong credentials!")

        # Leave the software.
        elif(menuOption == 'c' or menuOption == 'C'):
            leaveFlag = True
            print("Thanks, have a great time!")
            sys.exit()     

    # Step 2 - Service Interaction upon Sucessful Login or Account Creation.
    if(userLogged):

        # TODO: Service Interaction
        printMenu(4)
        menuOption = input()

        # Option 1
        if(menuOption == 'z' or menuOption == 'Z'):
            print("Service 1 - Folder Access")
            # Build M1 for As.py
            # M1 = [ID_C + {ID_S + T_R + N1}Kc]
            # ID_C = Identificador do cliente.
            # ID_S = Identificador do serviço pretendido.

            userTime = input("How long do you want to access? (Minutes): ")
            try:
                ticketTime = int(userTime)
            except ValueError:
                print("Invalid Time")
                sys.exit()

            # T_R = Tempo solicitado pelo Cliente para ter acesso ao serviço.
            # N1 = Número aleatório 1.
            # Kc = Chave do cliente (Somente o cliente e o AS conhecem).
            
            kc = password[:8]
            ID_C = username
            ID_S = 'AX_01'
            T_R = userTime
            N1 = str(secrets.randbelow(55555))
            # print("kc " + str(kc))
            # print("ID_C " + str(ID_C))
            # print("ID_S " + str(ID_S))
            # print("T_R " + str(T_R))
            # print("N1 " + str(N1))
            M1 = [ID_C, [encryptDES(ID_S,kc), encryptDES(T_R, kc), encryptDES(N1,kc) ]]

            # Send M1 to AS.py
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                soc.connect((ipHOST,ASPORT))
                M1data = pickle.dumps(M1)
                soc.sendall(M1data)
                print("M1 was sent to AS server;")
                
                # Wait for M2 from AS.py
                M2 = soc.recv(1024)
                M2 = pickle.loads(M2)

            # Verify if N1 is correct
            if(decryptDES(M2[0][1],kc).decode() != N1):
                
                # Wrong random number
                print("Wrong Number, Wrong Ticket m'buddy (N1)")
                sys.exit()
            print(" M2 received; ")
            # Build M3. Get's kc_tgs from M2 and build new N2.
            kc_tgs = decryptDES(M2[0][0],kc).decode()
            N2 = str(secrets.randbelow(55555))
            M3 = [[encryptDES(ID_C,kc_tgs),encryptDES(ID_S,kc_tgs),encryptDES(T_R,kc_tgs),encryptDES(N2,kc_tgs)],[M2[1][0],M2[1][1],M2[1][2]]]

            # Send M3 to TGS.py
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                soc.connect((ipHOST,TGSPORT))
                M3data = pickle.dumps(M3)
                soc.sendall(M3data)
                print("M3 was sent to TGS server;")
                
                # Wait for M4 from TGS.py
                M4 = soc.recv(1024)
                M4 = pickle.loads(M4)
            
            # print(decryptDES(M4[0][0],kc_tgs).decode())
            # print(decryptDES(M4[0][1],kc_tgs).decode())
            # print(decryptDES(M4[0][2],kc_tgs).decode())

            # Verify if N2 is correct;
            if(decryptDES(M4[0][2],kc_tgs).decode() != N2):

                # Wrong random number
                print("Wrong Number, Wrong Ticket m'buddy (N2)")
                sys.exit()

            print(" M4 received; ")
            kcs = decryptDES(M4[0][0],kc_tgs).decode()
            T_A = decryptDES(M4[0][1],kc_tgs).decode()
            S_R = 'f'

            print(" You have " + time.ctime(float(T_A)) + " remaining")

            # This ticket will be generated at all options on this service
            serviceUsage = True
            serviceAnswer = -1
            while serviceUsage:
                # Build M5: [{ID_C + (T_A ou T_R) + S_R + N3}K_c_s + T_c_s]                          
                N3 = str(secrets.randbelow(55555))
                M5 = [[encryptDES(ID_C,kcs),encryptDES(T_A,kcs),encryptDES(S_R,kcs),encryptDES(N3,kcs)],[M4[1][0],M4[1][1],M4[1][2]]]

                # Connect in Service Loop
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                    soc.connect((ipHOST,SPORT))
                    M5data = pickle.dumps(M5)
                    soc.sendall(M5data)
                    print(S_R)
                    print("M5 was sent to Services Server;")

                    # Wait for M6.
                    M6 = soc.recv(1024)
                    M6 = pickle.loads(M6)

                # Verify if N3 is correct;
                if(decryptDES(M6[1],kcs).decode() != N3):

                    # Wrong random number
                    print("Wrong Number, Wrong Ticket m'buddy (N3)")
                    serviceUsage = False
                    sys.exit()

                print(" M6 received; ")
                serviceAnswer = decryptDES(M6[0],kcs).decode()
                if(serviceAnswer == '000'):
                    print("Service timeout - Ticket expired.")
                    serviceUsage = False
                    sys.exit()

                if(serviceAnswer == '004'):
                    print("Thank you for using our service")
                    serviceUsage = False
                    sys.exit()
                else:
                    print(serviceAnswer)
                    S_R = input("__: ")

                    if(S_R == 'z' or S_R == 'Z'):
                        S_R = 'z'
                    elif(S_R == 'x' or S_R == 'X'):
                        S_R = 'x'
                    elif(S_R == 'c' or S_R == 'C'):
                        S_R = 'c'
                    else:
                        S_R = 'f'

        elif(menuOption == 'x' or menuOption == 'X'):
            print("Service 2 is not available right now.")
            sys.exit()
        elif(menuOption == 'c' or menuOption == 'x'):
            printMenu(6)
            sys.exit()

if __name__ == "__main__":
    main()