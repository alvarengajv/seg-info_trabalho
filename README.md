# Trabalho Prático: Implementação e Análise TCP vs TLS

**Disciplina:** Segurança da Informação  
**Professor:** Gabriel Rodrigues Caldas de Aquino  
**Alunos:** Antônio Nazar e João Vitor Alvarenga  

## 1. Visão Geral

Este projeto consiste na implementação de um cliente e servidor em Python para transferência de arquivos utilizando dois protocolos distintos:
1.  **TCP (Transmission Control Protocol):** Transmissão em texto claro (não seguro).
2.  **TLS (Transport Layer Security):** Transmissão criptografada e segura.

O objetivo é comparar o funcionamento, analisar o *overhead* introduzido pela criptografia e evidenciar as diferenças de segurança através da captura de pacotes.

## 2. Estrutura do Projeto

*   `tcp_server.py`: Servidor TCP simples.
*   `tcp_client.py`: Cliente TCP que envia um arquivo e mede o tempo de envio.
*   `tls_server.py`: Servidor seguro que utiliza certificados SSL/TLS.
*   `tls_client.py`: Cliente seguro que envia um arquivo criptografado.
*   `main.py`: Script de automação que executa os testes de ambas as modalidades sequencialmente.
*   `cert_gen.py`: Script auxiliar para gerar certificados (via biblioteca cryptography).
*   `test_file.txt`: Arquivo de exemplo para teste de transmissão.

## 3. Pré-requisitos

*   **Python 3.x** instalado.
*   Biblioteca **cryptography** (`pip install cryptography`).

## 4. Configuração Inicial (Certificados)

Para rodar a versão TLS, é necessário gerar um par de chaves (certificado público e chave privada). 

O script `main.py` irá gerar esses arquivos **automaticamente** caso eles não existam, utilizando o módulo auxiliar `cert_gen.py`.

Se desejar gerar manualmente:

```bash
python cert_gen.py
```

Isso criará dois arquivos na raiz do projeto:
*   `server.crt` (Certificado Público)
*   `server.key` (Chave Privada)

## 5. Como Executar

Você pode executar os clientes e servidores manualmente em terminais separados ou usar o script de automação.

### Modo Automático (Recomendado)
O script `main.py` sobe os servidores, executa os clientes e exibe o tempo de execução no console.

```bash
python main.py
```

### Modo Manual

**TCP (Terminal 1 - Servidor):**
```bash
python tcp_server.py
```
**TCP (Terminal 2 - Cliente):**
```bash
python tcp_client.py test_file.txt
```

**TLS (Terminal 1 - Servidor):**
```bash
python tls_server.py
```
**TLS (Terminal 2 - Cliente):**
```bash
python tls_client.py test_file.txt
```

## 6. Realizando a Captura de Pacotes (Wireshark)

Para o relatório, siga estes passos:

1.  Abra o **Wireshark**.
2.  Selecione a interface de loopback (geralmente chamada de "Adapter for loopback traffic capture" ou "lo0").
3.  Inicie a captura.
4.  Execute o script `python main.py`.
5.  Pare a captura.
6.  Utilize os filtros:
    *   `tcp.port == 5000` para ver o tráfego em texto claro.
    *   `tcp.port == 5001` para ver o tráfego criptografado (TLS).
7.  Analise o conteúdo dos pacotes (payload) para o relatório.

## 7. Resultados Esperados

*   **Conexão TCP:** Os dados do arquivo `test_file.txt` serão visíveis no corpo dos pacotes capturados.
*   **Conexão TLS:** Os dados trafegados estarão ilegíveis (criptografados) após o handshake TLS.
