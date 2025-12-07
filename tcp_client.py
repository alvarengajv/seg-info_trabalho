import socket
import time
import os
import sys

def send_file(filename, host='127.0.0.1', port=5000):
    if not os.path.exists(filename):
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return

    # Criar um socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP

    # Conectar o socket à porta onde o servidor está escutando
    server_address = (host, port)
    print(f"Conectando a {host}:{port}")
    
    try:
        sock.connect(server_address)
        
        start_time = time.time()
        
        print(f"Enviando {filename}...")
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sock.sendall(data)
                
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Arquivo enviado com sucesso.")
        print(f"Tempo decorrido (TCP): {duration:.6f} segundos")
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python tcp_client.py <arquivo>")
        print("Usando 'test_file.txt' padrão para fins de demonstração se existir.")
        send_file('test_file.txt')
    else:
        send_file(sys.argv[1])
