import socket
import threading
from time import sleep
import random
import string

HOST = "0.0.0.0"
PORT = 2223
N_RODADAS = 3

LETRA = ""
QTD_JOGADORES = 0

# As listas começam vazias e vão crescer dependendo de quantos jogarem
CEP = []
NOME = []
ANIMAL = []
COR = []
MSE = []
COMIDA = []

semaforo = threading.Semaphore(0)

def atender_cliente(conn, tid):
    global CEP, NOME, ANIMAL, COR, MSE, COMIDA, LETRA

    # Trava esperando a thread principal liberar o início da rodada
    semaforo.acquire()
    
    # Envia a letra sorteada ao cliente
    conn.sendall(LETRA.encode())

    # Recebe todas as respostas de uma vez (separadas por ';')
    resposta = conn.recv(1024).decode().split(";")
    
    # Salva no índice respectivo do jogador (tid)
    CEP[tid] = resposta[0]
    NOME[tid] = resposta[1]
    ANIMAL[tid] = resposta[2]
    COR[tid] = resposta[3]
    MSE[tid] = resposta[4]
    COMIDA[tid] = resposta[5]

def iniciar_servidor():
    global LETRA, QTD_JOGADORES, CEP, NOME, ANIMAL, COR, MSE, COMIDA
    
    # Pergunta quantos jogadores vão jogar logo que o servidor abre
    QTD_JOGADORES = int(input("Digite a quantidade de jogadores para esta partida: "))
    
    # Prepara as listas globais com espaços vazios para cada jogador
    CEP = [""] * QTD_JOGADORES
    NOME = [""] * QTD_JOGADORES
    ANIMAL = [""] * QTD_JOGADORES
    COR = [""] * QTD_JOGADORES
    MSE = [""] * QTD_JOGADORES
    COMIDA = [""] * QTD_JOGADORES

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"\nServidor ouvindo em {HOST}:{PORT}")
        print(f"Aguardando {QTD_JOGADORES} jogadores conectarem...")
        
        conexoes = []
        # Loop para aguardar a quantidade exata de jogadores definida
        for i in range(QTD_JOGADORES):
            conn, addr = server.accept()
            print(f"Jogador {i+1} conectou! IP: {addr}")
            conexoes.append(conn) # Guarda a conexão na lista

        # Lista para guardar a pontuação de cada jogador
        pontos_jogadores = [0] * QTD_JOGADORES

        # Loop de múltiplas rodadas
        for rodada in range(N_RODADAS):
            
            LETRA = random.choice(string.ascii_uppercase)
            print(f"\nRodada {rodada+1} iniciada! Letra sorteada: {LETRA}")

            threads = []
            # Cria uma thread para cada jogador que conectou
            for i in range(QTD_JOGADORES):
                t = threading.Thread(target=atender_cliente, args=(conexoes[i], i))
                threads.append(t)
                t.start()

            # Libera o semáforo para TODOS os jogadores andarem ao mesmo tempo
            for _ in range(QTD_JOGADORES):
                semaforo.release()

            # A thread principal aguarda todos os clientes enviarem as respostas
            for t in threads:
                t.join()

            # --- CÁLCULO DE PONTOS (Para N jogadores) ---
            categorias = [CEP, NOME, ANIMAL, COR, MSE, COMIDA]
            
            # Para cada jogador...
            for i in range(QTD_JOGADORES):
                # ...verifica cada uma de suas respostas
                for categoria in categorias:
                    resposta_do_jogador = categoria[i]
                    
                    # Se a resposta dele aparece só 1 vez na lista, é única (3 pontos)
                    if categoria.count(resposta_do_jogador) == 1:
                        pontos_jogadores[i] += 3
                    # Se aparece mais de 1 vez, alguém respondeu igual (1 ponto)
                    else:
                        pontos_jogadores[i] += 1

            # Monta o resultado final formatado para enviar aos clientes
            resultado = f"Rodada {rodada+1} | Placar: "
            for i in range(QTD_JOGADORES):
                resultado += f"J{i+1}: {pontos_jogadores[i]} pts | "
            
            # Envia o placar para todos
            for conn in conexoes:
                conn.sendall(resultado.encode())
            
            # Pausa rápida para o cliente processar
            sleep(0.5)

if __name__ == "__main__":
    iniciar_servidor()