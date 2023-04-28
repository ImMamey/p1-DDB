import socket
import threading

class Server:
    class Network:
        def __init__(self)-> None:
            self.SERVER: str = socket.gethostbyname(socket.gethostname()) # guarda IP del server
            self.PORT: int = 5555 #purto a usar
            self.ADDR: tuple = (self.SERVER, self.PORT) # guarda tupla (ip, puerto)
            self.FORMAT: str = 'utf-8' # encode type
            self.DISCONNECT_MESSAGE: str= "!DISCONNECT" # mensaje de desconecction
            self.HEADER: int =64

            self.server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # inicia un socket por TCP
            self.server.bind(self.ADDR)

    def handle_client(self, conn, addr,n):
        print(f"[NUEVA CONNECCION] {addr} connectado.")

        connected: bool = True
        while connected:
            msg_length= conn.recv(n.HEADER).decode(n.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(n.FORMAT)
                if msg == n.DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg}")
                conn.send("Msg recibido".encode(n.FORMAT))

    def start(self):
        n = self.Network()
        n.server.listen()
        print(f"[Escuchando] Servidor esta escuchando en. {n.SERVER}")
        while True:
            conn, addr = n.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr,n))
            thread.start()
            print(f"[CONNECIONES ACTIVAS] {threading.activeCount() - 1}")



if __name__ =="__main__":
    print("[INICIANDO SERVIDOR] el servidor está iniciando....")
    s = Server()
    s.start()