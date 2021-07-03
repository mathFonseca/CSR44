
import secrets
import sys
import cifrador
import numpy as np

# Leitura de Paramentro (Cifrar, Decifrar, Chave)
if len(sys.argv) <= 1:
    print("Wrong number of parameters.")
    sys.exit()

PARAMETER_LIST = sys.argv[1:]
INPUT_TEXT = sys.stdin.read()
OUTPUT_TEXT = ""

def vernam(inputText, typeMode = '-c', decryptionKey=None):
    outputText = []
    if(inputText is None):
        print("Input Text is None")
        return 0

    if(typeMode == '-d'):
        if(len(decryptionKey) != len(inputText)):
            print("Key Lenght is not the same")
            print("vernamKey: " + str(len(decryptionKey)) + " keyLenght: " + str(len(inputText)))
            return 0
        for cryptedLetter in range(len(inputText)):
            # Characters from vernamKey not in CHAR_LIST copy and paste
            if(decryptionKey[cryptedLetter] in cifrador.CHAR_LIST):
                originalLetter_index = ord(inputText[cryptedLetter]) - cifrador.CHAR_LIST.index(decryptionKey[cryptedLetter])                    
                if(cifrador.CHAR_LIST[originalLetter_index] in cifrador.CHAR_LIST):
                    outputText.append(cifrador.CHAR_LIST[originalLetter_index])
                else:
                    print("Resulted Letter not in range")
                    outputText.append('>')
            else:
                outputText.append(decryptionKey[cryptedLetter])
        return "".join(outputText)        
    else:
        keyLenght = len(inputText)
        cesarKey = secrets.randbelow(99999999)
        vernamKey = cifrador.cesar(inputText, "-c",KEY = cesarKey)
        if(len(vernamKey) != keyLenght):
            print("Key Lenght is not the same")
            return 0
        
        # Cifrando
        for letters in range(0,len(inputText)):
            # Posicao da Letra a ser Cifrada
            if(inputText[letters] in cifrador.CHAR_LIST):
                letterText_index = cifrador.CHAR_LIST.index(inputText[letters])
                letterKey_index = cifrador.CHAR_LIST.index(vernamKey[letters])
                newLetterIndex = letterText_index + letterKey_index
                outputText.append(chr(newLetterIndex))
            else:
                outputText.append(chr(letters))
            # Eis a questão: Se quisermos deixar bem dificil, podemos fazer com que o
            # resultado saia do esperado [A-Z,a-z,0-9], podendo cair até mesmo em char
            # incorreto. Seria uma tática de segurança extra.
            # Ou manter ainda dentro do nosso alfabeto original.
            # Aqui, implementamos uusando diretamente a tabela ASCII, permitindo que 
            # tenhamos literalmente qualquer coisa.

        with open('vernamKey.dat', 'w') as f:
            f.write(vernamKey)
        return "".join(outputText)
            
# Criptografa vernam
if PARAMETER_LIST[0] == '-c':
    OUTPUT_TEXT = vernam(INPUT_TEXT,PARAMETER_LIST[0])
    print(OUTPUT_TEXT)

# Descriptografa vernam (necessario encryptionKey)
elif PARAMETER_LIST[0] == '-d':
    with open('vernamKey.dat','r') as f:
        decryptionKey = f.read()
    # PRINT Function adds \n on the file. We need to remove it
    INPUT_TEXT = INPUT_TEXT[:len(INPUT_TEXT)-1]
    OUTPUT_TEXT = vernam(INPUT_TEXT,PARAMETER_LIST[0],decryptionKey)
    print(OUTPUT_TEXT)
