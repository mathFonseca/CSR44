# ------------------------------
# Trabalho 1 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Analisador de Frequencia.
# ------------------------------

import numpy as np
import sys


# Leitura de Paramentro (Iterações)

if len(sys.argv) == 1:
    print("Wrong number of parameters. Please use -c or -d, -k key-number ")
    sys.exit()

# Variáveis Globais
maxInterationsByUser = int(sys.argv[1])
decodeInterations = int(0)
INPUT_TEXT = sys.stdin.read()

CHAR_LIST = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
CHAR_LIST.extend(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])
CHAR_LIST.extend(['0','1','2','3','4','5','6','7','8','9'])

mostFrequentLetter_ptbr = ['a','e','o','s','r']

# Return the letter frequency of an given string / text in lowercase.
def frequency_counter(inputText):
    countList = [] 
    # For each character in our CHAR_LIST
    # Ignoring uppercase letters.
    for character in CHAR_LIST:
        # Count number of ocourrences in CRYPTOGRAPHED_TEXT
        characterCount = inputText.count(character)
        # If greater than 0 (at least once), add to our 
        if (characterCount) > 0:
            countList.append([character,characterCount])

    return countList

# Check frequency of characters:
charCountList = frequency_counter(INPUT_TEXT)
print('List of characters: ')
print(charCountList)
# Ordena lista por characters que mais aparecem dentro das sublistas (Posição 1)
charCountList.sort(key = lambda x: x[1],reverse=True)
print('Sorted List of characters: ')
print(charCountList)
# Decode

if(INPUT_TEXT is None):
        print('Error reading file')
        sys.exit()
for decodeInterations in range(maxInterationsByUser):
    
    cesar_letter_index = CHAR_LIST.index(charCountList[decodeInterations][0])
    normal_letter_index = CHAR_LIST.index(mostFrequentLetter_ptbr[decodeInterations])
    # transform characters from the in lowercases
    if(cesar_letter_index <= 25):
        cesar_letter_index += 26

    possible_cesar_key = cesar_letter_index - normal_letter_index
    # Volta completa da lista de char
    if(possible_cesar_key < 0):
        possible_cesar_key += len(CHAR_LIST)
    print('Possible Cesar Key number ' + str(decodeInterations) + ' : ' + str(possible_cesar_key))

