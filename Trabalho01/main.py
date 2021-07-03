# ------------------------------
# Trabalho 1 - Segurança de Redes e Sistemas
# Autor: Matheus Fonseca Alexandre de Oliveira
# Professor: Mauro Fonseca
# Projeto: Cifra de Cesar
# ------------------------------

# Rotação do Cifrador  [A-Z,a-z,0-9].
# Bibilotecas

import sys
import cifrador

# Leitura de Paramentro (Cifrar, Decifrar, Chave)
if len(sys.argv) <= 1:
    print("Wrong number of parameters.")
    sys.exit()
    

PARAMETER_LIST = sys.argv[1:]
INPUT_TEXT = sys.stdin.read()
OUTPUT_TEXT = ""

if PARAMETER_LIST[0] == '-c' or PARAMETER_LIST[0] == '-d':
    cesarMODE = str(PARAMETER_LIST[0])
    cesarKEY = int(PARAMETER_LIST[1])
    OUTPUT_TEXT = cifrador.cesar(INPUT_TEXT,cesarMODE,cesarKEY)
    print(OUTPUT_TEXT)

    
