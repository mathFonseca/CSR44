  
# ------------------------------
# Trabalho 2 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Gerador de OTP
# ------------------------------

# ------------------------------
# Especificação: Controle de Usuários
# Gerar até 5 OTP por vez, invalidar todas após
# primeiro uso de qualquer uma delas.
# Usar ano-mes-dia-hora-minuto-segundo na hash
# Usar Salt
# ------------------------------

# Bibliotecas

import csv
import datetime
import sys
import hashlib

def signUp(username, seed, localPassword):
    # Regiser user on database. Seed and localPassword needs to be
    # hashed and salted.

    with open('tokenDatabase.csv', 'a+', newline='') as tokenDatabase:
        newRow = csv.writer(tokenDatabase, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newRow.writerow([username, localPassword, seed])
    return

def signIn(username, localPassword):
    # User connect to generator do get OTP
    # Need to check if user is already registered:
    
    with open('tokenDatabase.csv','r', newline='') as tokenDatabase:
        dataLoad = csv.reader(tokenDatabase, delimiter=';', quotechar='"')
        for rowContent in dataLoad:
            # Check if user is registered on database
            if (rowContent[0] == username):
                if (rowContent[1] == localPassword):
                    # User found and with correct Password
                    return True
                else:
                    # Find a correct username but with Wrong Password
                    return False
        # Didn't find a correct username
        return False

def getSeed(username):
    # Given a username, get his seed on database
    with open('tokenDatabase.csv','r',newline='') as tokenDatabase:
        dataLoad = csv.reader(tokenDatabase, delimiter=';', quotechar='"')
        for rowContent in dataLoad:
            if(rowContent[0] == username):
                userSeed = rowContent[2]
                return userSeed
        return -1

def checkUsername(username):
    # Given a username, check if we have the username on database
    with open('tokenDatabase.csv','r',newline='') as tokenDatabase:
        dataLoad = csv.reader(tokenDatabase, delimiter=';', quotechar='"')
        for rowContent in dataLoad:
            if(rowContent[0] == username):
                return False
        return True

def generateOTP(username):
    # OTP Elements:
    # 1 - Hour on the system
    time_now = datetime.datetime.now()

    # Add time to the current seed
    # It's already salted
    user_seed = getSeed(username)

    if(user_seed == -1):
        print("Bad Seed!")
        sys.exit()

    user_seed = user_seed + str(time_now.year) + str(time_now.month) + str(time_now.day) + str(time_now.hour) + str(time_now.minute)

    # Create 5 OTP
    otp_1 = hashlib.sha256(user_seed.encode()).hexdigest()
    otp_2 = hashlib.sha256(otp_1.encode()).hexdigest()
    otp_3 = hashlib.sha256(otp_2.encode()).hexdigest()
    otp_4 = hashlib.sha256(otp_3.encode()).hexdigest()
    otp_5 = hashlib.sha256(otp_4.encode()).hexdigest()

    # Print everything for the user
    print("The follwing OTP are valid from " + str(time_now.year) + "-" + str(time_now.month) + "-" + str(time_now.day) + " " + str(time_now.hour) + ":" + str(time_now.minute))
    print("They last for 1 minute.")
    print("OTPs: \n" + otp_1[:8] + "\n" + otp_2[:8] + "\n" + otp_3[:8] + "\n" + otp_4[:8] + "\n" + otp_5[:8] + "\n")
            
def updateAppDatabase(username, userSeed):
    # Send to app database the user and the userSeed
    with open('appDatabase.csv', 'a+', newline='') as appDatabase:
        newRow = csv.writer(appDatabase, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        newRow.writerow([username, userSeed])
def main():

    print(" Welcome to OTP Generator")
    print(" Please choose:")
    print(" 1 - Create User")
    print(" 2 - Generate OTP")
    print(" 0 - Leave")
    menu = input()

    if(menu == '0'):
        sys.exit()
    elif(menu == '1'):
        # SignUp Step
        usernameData = input("Username: ")
        userLocalPassword = input("Local Password: ")
        userSeed = input("Master Password: ")

        if(checkUsername(usernameData)):
            # Calculate Unique Salt for the user:
            userSalt = str(usernameData)[::-1]

            # Add Salt to Passwords:
            userLocalPassword += userSalt
            userSeed += userSalt

            # Hashes both passwords for Sign Up
            userLocalPassword = hashlib.sha256(userLocalPassword.encode()).hexdigest()
            userSeed = hashlib.sha256(userSeed.encode()).hexdigest()

            # Update our database and app database with new user.
            signUp(usernameData, userSeed, userLocalPassword)
            updateAppDatabase(usernameData, userSeed)

            print("Sign Up OK! Welcome!")
        else:
            print("Username already taken, try again!")
            sys.exit()
    elif(menu == '2'):
        # SignIn Step
        usernameData = input(" Username: ")
        userLocalPassword = input(" Local Password: ")

        # Calculate Unique Salt for the user:
        userSalt = str(usernameData)[::-1]

        # Add Salt to Passwords:
        userLocalPassword += userSalt

        # Hash the local password
        userLocalPassword = hashlib.sha256(userLocalPassword.encode()).hexdigest()

        if (signIn(usernameData, userLocalPassword)):
            # Successful signIn
            print(" Good! Welcome!")
            print(" Please choose:")
            print(" 1 - Generate OTP")
            print(" 0 - Exit")

            menu = input()
            if(menu == '1'):
                generateOTP(usernameData)
            else:
                sys.exit()
        else:
            # Not so successful sign in
            print(" Uh, Bad! The credentials don't match, Try again")
            sys.exit()
    else:
        print("Wrong input")
        sys.exit()

if __name__ == "__main__":
    main()

