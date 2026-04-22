import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

# Estruturas globais
fila_mensagens = []
clientes_recebimento = []

# Semáforos para proteger o acesso concorrente (Requisito obrigatório)
semaforo_fila = threading.Semaphore(1)
semaforo_clientes = threading.Semaphore(1)
itens_na_fila = threading.Semaphore(0)

def tratar_cliente(conn, addr):
    """Lida com cada cliente conectado em uma thread dedicada"""
    global fila_mensagens, clientes_recebimento
    
    try:
        # Aguarda a primeira mensagem para definir o tipo de cliente (Handshake)
        dados_iniciais = conn.recv(1024).decode()
        
        if dados_iniciais.startswith("TIPO:ENVIO"):
            # Extrai o nome do cliente que foi enviado antes das mensagens
            nome = dados_iniciais.split(";")[1].split(":")[1]
            print(f"[+] Cliente de ENVIO conectado: {nome} | IP: {addr[0]}")
            
            # Loop (Executam em loop) - Recebe mensagens do cliente
            while True:
                msg = conn.recv(1024).decode()
                if not msg:
                    break
                
                # Formata a mensagem com Nome, IP e Horário
                horario = datetime.now().strftime("%H:%M:%S")
                msg_formatada = f"[{nome} ({addr[0]}) {horario} ]\n{msg}\n"
                
                # Inclui a mensagem na fila protegendo contra acesso concorrente com semáforo
                semaforo_fila.acquire()
                fila_mensagens.append(msg_formatada)
                semaforo_fila.release()
                
                # Sinaliza (libera) para a thread de distribuição que há uma nova mensagem
                itens_na_fila.release()
                
                # Retorna ao cliente a confirmação (Conforme diagrama)
                conn.sendall("OK".encode())
                
        elif dados_iniciais.startswith("TIPO:RECEBIMENTO"):
            print(f"[+] Cliente de RECEBIMENTO conectado | IP: {addr[0]}")
            
            # Adiciona na lista de clientes que vão receber o broadcast do servidor
            semaforo_clientes.acquire()
            clientes_recebimento.append(conn)
            semaforo_clientes.release()
            
            # Mantém a conexão aberta para o servidor conseguir "empurrar" as mensagens
            while True:
                if not conn.recv(1024):
                    break

    except Exception as e:
        print(f"[-] Conexão encerrada com {addr[0]}")
    finally:
        # Limpeza caso o cliente desconecte
        semaforo_clientes.acquire()
        if conn in clientes_recebimento:
            clientes_recebimento.remove(conn)
        semaforo_clientes.release()
        conn.close()

def distribuir_mensagens():
    """Thread que executa em loop retirando mensagens da fila e enviando a todos"""
    while True:
        # Aguarda até que haja pelo menos uma mensagem na fila
        itens_na_fila.acquire()
        
        # Retira a mensagem da fila com segurança
        semaforo_fila.acquire()
        if fila_mensagens:
            msg = fila_mensagens.pop(0)
        else:
            msg = None
        semaforo_fila.release()
        
        if msg:
            # Envia a mensagem retirada a todos os clientes de recebimento
            semaforo_clientes.acquire()
            clientes_desconectados = []
            
            for cliente in clientes_recebimento:
                try:
                    cliente.sendall(msg.encode())
                except:
                    clientes_desconectados.append(cliente)
            
            # Remove clientes que caíram/fecharam o terminal
            for c in clientes_desconectados:
                clientes_recebimento.remove(c)
            
            semaforo_clientes.release()

def iniciar_servidor():
    # Inicia a thread separada responsável por esvaziar a fila e fazer o broadcast
    t_distribuicao = threading.Thread(target=distribuir_mensagens, daemon=True)
    t_distribuicao.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        
        print(f"Servidor de Mensagens rodando na porta {PORT}")
        print("Aguardando conexões...\n")
        
        while True:
            conn, addr = servidor.accept()
            # Múltiplos clientes simultaneamente utilizando threads
            t = threading.Thread(target=tratar_cliente, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    iniciar_servidor()