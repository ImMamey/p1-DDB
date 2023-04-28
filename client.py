import socket
import pickle


class Network:
    def __init__(self) -> None:
        """

        :var client
        """
        self.client: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #inicia socket TCP
        self.server: str = socket.gethostname() # guarda IP del server
        self.port: int = 5555 # puerto para el socket
        self.addr: tuple = (self.server, self.port) # guarda tupla con datos de (ip, puerto)
        self.p = self.connect() # inicia connection

    def getP(self):
        return self.p
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Fallo al conectarse al cliente. Para mas informacion: \n{exception}")
    def send(self, data):
        try:
            self.client.send(pickle.dumps(pickle.dumps(data)))
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Fallo al enviar packete: \n{exception}")

def main():
    run=True
    n: classmethod = Network()
    p= n.getP()

    while run:
        pass

