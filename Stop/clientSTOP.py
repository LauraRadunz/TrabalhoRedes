import socket
import unicodedata
import re

def limpar_resposta(texto):
    texto = texto.upper()
    nfkd = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    texto_limpo = re.sub(r'[^A-Z]', '', texto_sem_acento)

    return texto_limpo

HOST = "127.0.0.1"
PORT = 2223
N_RODADAS = 3

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    for rodada in range(N_RODADAS):
        letra = cliente.recv(1024).decode()
        print("\nLetra sorteada: " + letra) 

        respostaCEP = input("CEP: ")
        respostaNOME = input("Nome: ")
        respostaANIMAL = input("Animal: ")
        respostaCOR = input("Cor: ")
        respostaMSE = input("Minha sogra é: ")
        respostaCOMIDA = input("Comida: ")

        respostaCEP = limpar_resposta(respostaCEP)
        respostaNOME = limpar_resposta(respostaNOME)
        respostaANIMAL = limpar_resposta(respostaANIMAL)
        respostaCOR = limpar_resposta(respostaCOR)
        respostaMSE = limpar_resposta(respostaMSE)
        respostaCOMIDA = limpar_resposta(respostaCOMIDA)

        respostas = respostaCEP + ";" + respostaNOME + ";" + respostaANIMAL + ";" + respostaCOR + ";" + respostaMSE + ";" + respostaCOMIDA
        
        cliente.sendall(respostas.encode())

        resultado = cliente.recv(1024).decode()
        print(resultado)

