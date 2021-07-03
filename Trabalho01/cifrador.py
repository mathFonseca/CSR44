# ------------------------------
# Trabalho 1 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Cifra de Cesar
# ------------------------------

# Rotação do Cifrador  [A-Z,a-z,0-9].
# Bibilotecas
import numpy as np

# Variaveis Globais
KEY = 0 # Chave 
CHAR_LIST = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
CHAR_LIST.extend(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])
CHAR_LIST.extend(['0','1','2','3','4','5','6','7','8','9'])

# Cifrador e Decifrador de Cesar.
#   MODE = -c ou -d para Cifrar ou Decifrar. Default: Cifrar
#   KEY = Chave correspondente. Default: 0
#   INPUT_TEXT = Texto de entrada
#   ALPHABET = Alfabeto para cifrar. Default: A-Z,a-z,0-9
#   Todas as letras do texto de entrada precisam estar 
#   contidas no alfabeto.
def cesar(INPUT_TEXT, MODE = '-c', KEY = '0', ALPHABET = None):

    # Variaveis Internas    
    OUTPUT_TEXT = []
    Sucess = False

    # Checagem de valores de entrada
    if(INPUT_TEXT is None):
        print("Input Text is None")
        return 0
    if(ALPHABET is None):
        ALPHABET = CHAR_LIST

    # Ajustamos a chave
    if( KEY >= len(ALPHABET)):
        amount = np.floor(KEY/len(ALPHABET))
        KEY -= int(amount*len(ALPHABET))  
    # Cifrador
    if(MODE == '-c'):
        for letter in INPUT_TEXT:
            # Pula characters incorretos
            if(letter in ALPHABET):
                letter_index = ALPHABET.index(letter)
                new_letter_index = letter_index + KEY
                # Checar se não vai passar do limite
                if(new_letter_index >= len(ALPHABET)):
                    # Checamos o que resta
                    new_letter_index = new_letter_index - len(ALPHABET)
                # Por removermos voltas múltiplas, a new_letter_index vai cair dentro da nossa lista   
                OUTPUT_TEXT.append(ALPHABET[new_letter_index])
            else:
                # Character incorreto deixamos onde estava            
                OUTPUT_TEXT.append(letter)
        Sucess = True        
    elif(MODE == '-d'):
        for letter in INPUT_TEXT:
            if(letter in ALPHABET):
                letter_index = ALPHABET.index(letter)
                new_letter_index = letter_index - KEY
                if(new_letter_index < 0):
                    new_letter_index = len(ALPHABET) + new_letter_index
                OUTPUT_TEXT.append(ALPHABET[new_letter_index])
            else:
                OUTPUT_TEXT.append(letter)
        Sucess = True
    else:
        print("Incorrect MODE parameter")
        Sucess = False
        return 0
    
    if(Sucess == True):
        return "".join(OUTPUT_TEXT)
    else:
        return 0

