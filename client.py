import socket


class Client:
    def __init__(self) -> None:
        self.HEADER: int = 64
        self.PORT: int = 5555
        self.FORMAT: str = 'utf-8'
        self.DISCONNECT_MESSAGE: str = "!DISCONNECT"
        self.SERVER: str = "192.168.56.1"
        self.ADDR: tuple = (self.SERVER, self.PORT)

        self.start()

    def start(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al tratar de conectarse al servidor: \n{exception}")


    def send(self, msg) -> None:
        try:
            message = msg.encode(self.FORMAT)  # encode el mensaje con el formato utf-8
            msg_length = len(message)  # calcula cantidad de caracteres en el mensaje
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
            print(self.client.recv(2048).decode(self.FORMAT))
        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al enviar el mensaje: \n{exception}")


if __name__ == "__main__":
    cl = Client()
    detente: bool = False

    while not detente:
        msg: str = input("Escriba un mensaje para enviar al Servidor (escriba \"n\" para detener)\n")
        if msg=="n":
            detente=True
            cl.send(cl.DISCONNECT_MESSAGE)
        else:
            cl.send(str(msg))