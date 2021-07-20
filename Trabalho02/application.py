  
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
import datetime
import hashlib
import sys
import csv


def getSeed(username):
    # Given a username, get his seed on database
    with open('appDatabase.csv','r',newline='') as appDatabase:
        dataLoad = csv.reader(appDatabase, delimiter=';', quotechar='"')
        for rowContent in dataLoad:
            if(rowContent[0] == username):
                userSeed = rowContent[1]
                return userSeed
        return -1

def generateOTP(username):
    # OTP Elements:
    # 1 - Hour on the system
    time_now = datetime.datetime.now()

    # Add time to the current seed
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

    # Return the list
    tokenList = [otp_1[:8], otp_2[:8], otp_3[:8], otp_4[:8], otp_5[:8]]
    return tokenList

def getUser(username):
    # Given a username, check if we have the username on database
    with open('appDatabase.csv','r',newline='') as appDatabase:
        dataLoad = csv.reader(appDatabase, delimiter=';', quotechar='"')
        for rowContent in dataLoad:
            if(rowContent[0] == username):
                return True
        return False

def updateUsedTokenList(tokenList):
    # Add entire list of tokens generated to file
    with open('invalidTokens','a+') as tokens:
        for items in tokenList:
            tokens.write("%s\n" % items)    

def verifyToken(tokenList, userToken):
    # Given an user token, verify if it's valid

    with open('invalidTokens') as tokens:
        invalidTokens = tokens.readlines()

    invalidTokens = [x.strip() for x in invalidTokens]

    for items in invalidTokens:
        if(items == userToken):
            print("Token Already Used")
            return False

    # If token are not in invalid list, check if inside user token List
    for token in tokenList:
        if(token == userToken):
            # Update the invalid List
            updateUsedTokenList(tokenList[tokenList.index(token):])
            return True
    
    # Update the invalid List
    updateUsedTokenList(tokenList[tokenList.index(token):])
    return False

def main():

    usernameData = input("Username: ")
    otpPassword = input("OTP Password: ")

    # Verify if user exist on app data or "server"
    if(getUser(usernameData)):        
        # Generate tokens
        tokenList = generateOTP(usernameData)

        # Verify if Token is correct
        if(verifyToken(tokenList, otpPassword)):
            # Token is valid, it's a verified user.
            print("Token is valid, congratulations!")
        else:
            # Token is not valid
            print("Token is not valid!")
            sys.exit()


    else:
        print("User not found! Register yourself in OTP App")
        sys.exit()


if __name__ == "__main__":
    main()