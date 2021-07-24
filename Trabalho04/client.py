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
        print("====== Welcome! " + str(username) + ", please select options below: ======")
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

# TODO: Implement
def signIn(username, password):
    columnOrder= ["username","password"]
    userData = pd.read_csv("userDatabase.csv", usecols=columnOrder)
    print(userData)

# Register new user on database
def signUp(username, password):
    with open('userDatabase.csv', 'a+', newline='') as userDatabase:
        newRow = csv.writer(userDatabase, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newRow.writerow([username, password])
    return

# Verify if username is available
def verifyUsername(username):
    columnOrder = ["username","password"]
    data = pd.read_csv("userDatabase.csv", usecols=columnOrder)
    for user in data["username"]:
        if user == username:
            return False
    return True

# Send userdata to AS database
def send2AS(username,password):
    with open('ASDatabase.csv', 'a+', newline='') as ASDatabase:
        newRow = csv.writer(ASDatabase, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newRow.writerow([username, password])
    return

def main():
    # TODO: Validate servers

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
            # TODO: Message to server.
            print("Service 1")
        elif(menuOption == 'x' or menuOption == 'X'):
            # TODO: Message to server.
            print("Service 2")
        elif(menuOption == 'c' or menuOption == 'x'):
            printMenu(6)
            sys.exit()

if __name__ == "__main__":
    main()