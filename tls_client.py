import socket
import ssl
import time
import os
import sys

def send_file_tls(filename, host='127.0.0.1', port=5001):
    if not os.path.exists(filename):
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return

    # Criar contexto SSL
    # Para certificados autoassinados neste trabalho, desabilitamos a verificação
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Criar um socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar o socket à porta onde o servidor está escutando
    server_address = (host, port)
    print(f"Conectando a {host}:{port} (TLS)")
    
    try:
        # Connect raw socket first
        sock.connect(server_address)
        
        # Envolver o socket
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            print(f"Conexão TLS estabelecida. Cifra: {ssock.cipher()}")
            
            start_time = time.time()
            
            print(f"Enviando {filename}...")
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    ssock.sendall(data)
                    
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"Arquivo enviado com sucesso.")
            print(f"Tempo decorrido (TLS): {duration:.6f} segundos")
            
    except ConnectionRefusedError:
        print(f"Erro: Não foi possível conectar a {host}:{port}. O servidor está rodando?")
    except ssl.SSLError as e:
        print(f"Erro SSL: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python tls_client.py <arquivo>")
        print("Usando 'test_file.txt' padrão para fins de demonstração.")
        send_file_tls('test_file.txt')
    else:
        send_file_tls(sys.argv[1])
