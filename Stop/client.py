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
        # Recebe a letra e avisa que o jogo liberou
        letra = cliente.recv(1024).decode()
        # Corrigido: concatenação no Python é com + e não com .
        print("\nLetra sorteada: " + letra) 

        # Jogador responde tudo localmente primeiro
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

        # Junta todas as respostas separadas por ;
        respostas = respostaCEP + ";" + respostaNOME + ";" + respostaANIMAL + ";" + respostaCOR + ";" + respostaMSE + ";" + respostaCOMIDA
        
        # Envia tudo de uma vez
        cliente.sendall(respostas.encode())

        # Fica travado aguardando o resultado
        resultado = cliente.recv(1024).decode()
        print(resultado)

        
