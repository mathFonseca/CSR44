# ------------------------------
# Trabalho 1 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Cifra de Cesar
# ------------------------------

# Rotação do Cifrador  [A-Z,a-z,0-9].
# Bibilotecas

import sys
import numpy as np

# Variaveis Globais
KEY = 0 # Chave 
CHAR_LIST = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
CHAR_LIST.extend(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])
CHAR_LIST.extend(['0','1','2','3','4','5','6','7','8','9'])

# Leitura de Paramentro (Cifrar, Decifrar, Chave)

if len(sys.argv) == 3:
    print("Wrong number of parameters. Please use -c or -d, -k key-number ")
    sys.exit()

PARAMETER_LIST = sys.argv[1:]
KEY = int(PARAMETER_LIST[2])
INPUT_TEXT = sys.stdin.read()
OUTPUT_TEXT = []

# Ajuste da chave.
# Como 62 é uma volta completa, só precisamos trabalhar com chaves menores que 62
if( KEY >= len(CHAR_LIST)):
    amount = np.floor(KEY/len(CHAR_LIST))
    KEY -= amount*len(CHAR_LIST)

# Decifrador / Cifrador
if PARAMETER_LIST[0] == '-c':
    for letter in INPUT_TEXT:
        # Pula characters incorretos
        if(letter in CHAR_LIST):
            letter_index = CHAR_LIST.index(letter)
            new_letter_index = letter_index + KEY
            # Checar se não vai passar do limite
            if(new_letter_index >= len(CHAR_LIST)):
                # Checamos o que resta
                new_letter_index = new_letter_index - len(CHAR_LIST)
            # Por removermos voltas múltiplas, a new_letter_index vai cair dentro da nossa lista 
            OUTPUT_TEXT.append(CHAR_LIST[new_letter_index])
        else:
            # Character incorreto deixamos onde estava            
            OUTPUT_TEXT.append(letter)
elif PARAMETER_LIST[0] == '-d':
    for letter in INPUT_TEXT:
        if(letter in CHAR_LIST):
            letter_index = CHAR_LIST.index(letter)
            new_letter_index = letter_index - KEY
            if(new_letter_index < 0):
                new_letter_index = len(CHAR_LIST) + new_letter_index
            OUTPUT_TEXT.append(CHAR_LIST[new_letter_index])
        else:
            OUTPUT_TEXT.append(letter)
else:
    print("Wrong parameter. Try again")
# Transform the output list in one string back again
print("".join(OUTPUT_TEXT))
