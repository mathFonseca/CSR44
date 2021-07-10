  
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
            
def main():

    # SignUp Step
    usernameData = input("Username: ")
    userLocalPassword = input("Local Password: ")

    signUp(usernameData, 'seedHashed', userLocalPassword)

    # SignIn Step
    if (signIn(usernameData, userLocalPassword)):
        # Successful signIn
        print("Good!")
    else:
        # Not so successful sign in
        print("Bad!")

if __name__ == "__main__":
    main()

