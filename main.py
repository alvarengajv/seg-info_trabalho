import subprocess
import time
import sys
import threading

def run_server(script_name):
    # Iniciar o script do servidor
    # Usamos o executável python explicitamente
    cmd = [sys.executable, script_name]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def run_client(script_name, filename='test_file.txt'):
    # Executar o script do cliente
    cmd = [sys.executable, script_name, filename]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Cliente falhou: {e.stderr}"

def tcp():
    print("--- Implementação TCP ---")
    server_process = run_server('tcp_server.py')
    
    # Dar tempo para o servidor iniciar
    time.sleep(2)
    
    # Executar cliente
    print("Executando Cliente TCP...")
    output = run_client('tcp_client.py')
    print(output)
    
    # Limpar servidor
    server_process.terminate()
    try:
        server_process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        server_process.kill()
    print("TCP Finalizado.\n")

def tls():
    print("--- Implementação TLS ---")
    # Verificar se certificados existem
    import os
    if not os.path.exists('server.crt') or not os.path.exists('server.key'):
        print("Certificados não encontrados. Tentando gerar automaticamente via cert_gen.py...")
        try:
            import cert_gen
            cert_gen.generate_certificates()
        except Exception as e:
            print(f"Falha ao gerar certificados automaticamente: {e}")
            return

    server_process = run_server('tls_server.py')
    
    # Dar tempo para o servidor iniciar
    time.sleep(2)
    
    # Executar cliente
    print("Executando Cliente TLS...")
    output = run_client('tls_client.py')
    print(output)
    
    # Limpar servidor
    server_process.terminate()
    try:
        server_process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        server_process.kill()
    print("TLS Finalizado.\n")

if __name__ == "__main__":
    # tcp()
    tls()
