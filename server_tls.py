import socket
import ssl

HOST = 'localhost'
PORT = 8443
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((HOST, PORT))
        sock.listen(1)
        print(f"Servidor aguardando conexões em {HOST}:{PORT}")
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        
        ssl_sock = context.wrap_socket(sock, server_side=True)
        
        print("Socket TLS configurado. Aguardando handshake...")
        
        while True:
            try:
                conn, addr = ssl_sock.accept()
                print(f"Conexão estabelecida com {addr}")
                
                data = conn.recv(1024)
                if data:
                    mensagem = data.decode('utf-8')
                    print(f"Mensagem recebida: {mensagem}")
                    
                    resposta = f"Servidor TLS responde: Mensagem recebida com sucesso!"
                    conn.send(resposta.encode('utf-8'))
                    print("Resposta enviada ao cliente")
                
                conn.close()
                print(f"Conexão com {addr} finalizada")
                
            except KeyboardInterrupt:
                print("\nServidor encerrado")
                break
            except Exception as e:
                print(f"Erro: {e}")
                continue
                
    finally:
        sock.close()

if __name__ == "__main__":
    main()
