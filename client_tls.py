import socket
import ssl

HOST = 'localhost'
PORT = 8443
CA_CERT = 'server.crt'

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(CA_CERT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED
        
        print(f"Conectando ao servidor {HOST}:{PORT}")
        
        ssl_sock = context.wrap_socket(sock, server_hostname=HOST)
        ssl_sock.connect((HOST, PORT))
        
        print("Conexão TLS estabelecida com sucesso!")
        print(f"Versão do TLS: {ssl_sock.version()}")
        print(f"Cipher suite: {ssl_sock.cipher()}")
        
        mensagem = "Olá, servidor TLS! Esta é uma mensagem segura."
        ssl_sock.send(mensagem.encode('utf-8'))
        print(f"Mensagem enviada: {mensagem}")
        
        resposta = ssl_sock.recv(1024)
        print(f"Resposta recebida: {resposta.decode('utf-8')}")
        
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        ssl_sock.close()
        print("Conexão fechada")

if __name__ == "__main__":
    main()
