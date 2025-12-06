import socket
import sys

def run_server(host='127.0.0.1', port=5000, output_file='received_file_tcp.txt'):
    # Criar um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Vincular o socket à porta
    server_address = (host, port)
    print(f"Iniciando servidor TCP em {host}:{port}")
    try:
        server_socket.bind(server_address)
    except OSError as e:
        print(f"Erro ao vincular à porta {port}: {e}")
        return

    # Escutar conexões recebidas
    server_socket.listen(1)
    
    print("Aguardando conexão...")
    
    while True:
        try:
            connection, client_address = server_socket.accept()
            print(f"Conexão de {client_address}")
            
            with connection:
                with open(output_file, 'wb') as f:
                    while True:
                        data = connection.recv(4096)
                        if not data:
                            break
                        f.write(data)
            print(f"Arquivo recebido e salvo em {output_file}")
            # Garantir fechamento adequado e encerrar para este exemplo simples
            break 
            
        except Exception as e:
            print(f"Erro durante a conexão: {e}")
            break
        finally:
            # A limpeza é tratada pelo 'with connection', mas mantido aqui por clareza
            pass
    
    server_socket.close()
    print("Servidor finalizado.")

if __name__ == "__main__":
    run_server()
