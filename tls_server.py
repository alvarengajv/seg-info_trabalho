import socket
import ssl
import sys

def run_tls_server(host='127.0.0.1', port=5001, output_file='received_file_tls.txt', certfile='server.crt', keyfile='server.key'):
    # Criar um contexto válido para o servidor
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    try:
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    except FileNotFoundError:
        print(f"Erro: Arquivos de certificado '{certfile}' e/ou '{keyfile}' não encontrados.")
        print("Por favor, execute 'cert_gen.py' ou gere-os manualmente.")
        return

    # Criar um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Vincular o socket à porta
    server_address = (host, port)
    print(f"Iniciando servidor TLS em {host}:{port}")
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
            
            # Envolver o socket com SSL
            try:
                # server_side=True é crucial aqui
                with context.wrap_socket(connection, server_side=True) as ssock:
                    print(f"Handshake TLS bem-sucedido com {client_address}")
                    with open(output_file, 'wb') as f:
                        while True:
                            data = ssock.recv(4096)
                            if not data:
                                break
                            f.write(data)
                    print(f"Arquivo recebido e salvo em {output_file}")
                    break # Uma requisição para este exemplo
            except ssl.SSLError as e:
                print(f"Erro SSL: {e}")
            except Exception as e:
                print(f"Erro ao lidar com a conexão: {e}")
                
        except Exception as e:
            print(f"Erro durante o aceite: {e}")
            break
            
    server_socket.close()
    print("Servidor finalizado.")

if __name__ == "__main__":
    run_tls_server()
