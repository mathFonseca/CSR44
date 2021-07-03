# ------------------------------
# Trabalho 1 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Analisador de Frequencia.
# ------------------------------

import cifrador
import sys

# Leitura de Paramentro (Cifrar, Decifrar, Chave)
if len(sys.argv) <= 1:
    print("Wrong number of parameters.")
    sys.exit()
mostFrequentLetter_ptbr = ['a','e','o','s','r']

PARAMETER_LIST = sys.argv[1:]
INPUT_TEXT = sys.stdin.read()
OUTPUT_TEXT = ""
PRINT_ENABLE = 0



# Return the letter frequency of an given string / text in lowercase.
def frequency_counter(inputText):
    countList = [] 
    # For each character in our CHAR_LIST
    # Ignoring uppercase letters.
    for character in cifrador.CHAR_LIST:
        # Count number of ocourrences in CRYPTOGRAPHED_TEXT
        characterCount = inputText.count(character)
        # If greater than 0 (at least once), add to our 
        if (characterCount) > 0:
            countList.append([character,characterCount])

    return countList

def analisador(inputText, maxInterationsByUser = 1, printResults = 0):

    possible_cesar_key = -1

    if(inputText is None):
        print("Please input text to analize.")
        return -1

    decodeInterations = int(0)
    charCountList = frequency_counter(inputText)
    if printResults == 1:
        print('List of characters: ')
        print(charCountList)

    charCountList.sort(key = lambda x: x[1],reverse=True)
    if printResults == 1:
        print('Sorted List of characters: ')
        print(charCountList)

    for decodeInterations in range(maxInterationsByUser):
        cesar_letter_index = cifrador.CHAR_LIST.index(charCountList[decodeInterations][0])
        normal_letter_index = cifrador.CHAR_LIST.index(mostFrequentLetter_ptbr[decodeInterations])
        # transform characters from the in lowercases
        if(cesar_letter_index <= 25):
            cesar_letter_index += 26

        possible_cesar_key = cesar_letter_index - normal_letter_index
        # Volta completa da lista de char
        if(possible_cesar_key < 0):
            possible_cesar_key += len(cifrador.CHAR_LIST)
        if printResults == 1:
            print('Possible Cesar Key number ' + str(decodeInterations) + ' : ' + str(possible_cesar_key))

    if(possible_cesar_key < 0):
        print("Error -1")
        return -1
    else:
        return possible_cesar_key

if('-p' in PARAMETER_LIST):
    PRINT_ENABLE = 1


if( len(PARAMETER_LIST) > 1):
    possible_key = analisador(INPUT_TEXT,printResults=1)
else:
    possible_key = analisador(INPUT_TEXT)
print("Possible Cesar key: " + str(possible_key))


