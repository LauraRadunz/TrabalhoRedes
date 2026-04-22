import socket

HOST = '127.0.0.1'
PORT = 5000

def iniciar_cliente_recebimento():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        
        # Handshake informando ao servidor que este é um processo de RECEBIMENTO
        handshake = "TIPO:RECEBIMENTO"
        cliente.sendall(handshake.encode())
        
        print(". ݁₊ ⊹ . ݁ Tela de mensagens ݁ . ⊹ ₊ ݁.")
        
        # Executa em loop (Conforme diagrama)
        while True:
            # Recebe mensagens formatadas do servidor
            msg = cliente.recv(4096).decode()
            
            if not msg:
                print("\nConexão com o servidor encerrada.")
                break
            
            print(msg)
            


if __name__ == "__main__":
    iniciar_cliente_recebimento()