import socket

HOST = '127.0.0.1'
PORT = 5000

def iniciar_cliente_envio():
    nome = input("Digite seu nome antes de entrar no chat: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        try:
            cliente.connect((HOST, PORT))
            
            nome = f"TIPO:ENVIO;NOME:{nome}"
            cliente.sendall(nome.encode())
            
            print(f"\nConectado como '{nome}'. Você já pode enviar mensagens.")

            while True:
                msg = input("Mensagem: ")
                
                if msg.strip() == "":
                    continue
                    
                # Envia mensagem ao servidor
                cliente.sendall(msg.encode())
                
                # Recebe confirmação (Conforme diagrama)
                confirmacao = cliente.recv(1024).decode()
                if confirmacao == "OK":
                    pass # Silenciado para manter o terminal de envio limpo
        
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar ao servidor. Verifique se ele está rodando.")

if __name__ == "__main__":
    iniciar_cliente_envio()