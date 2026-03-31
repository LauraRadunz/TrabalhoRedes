import socket

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

        # Junta todas as respostas separadas por ;
        respostas = respostaCEP + ";" + respostaNOME + ";" + respostaANIMAL + ";" + respostaCOR + ";" + respostaMSE + ";" + respostaCOMIDA
        
        # Envia tudo de uma vez
        cliente.sendall(respostas.encode())

        # Fica travado aguardando o resultado
        resultado = cliente.recv(1024).decode()
        print(resultado)