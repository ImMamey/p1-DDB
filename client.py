import socket
# TODO: en main se debe de preguntar por el ip del servidor para el constructor.

class Client:
    """
    Contiene todos los metodos para el cliente.
    """
    def __init__(self) -> None:
        """
        :var HEADER: Numero de bytes usado para algoritmo logico = como no sabemos cual es el tamaño de cada mensaje, todos los mensajes seran de 64 bytes. Facilita el encode/decode.
        :var PORT: Numero de puerto a usar.
        :var FORMAT: Formato de encode.
        :var DISCONNECT_MESSAGE: mensaje para la desconneción y cierre de sesion.
        :var SERVER: IP del servidor.
        :var ADDR: tupla con el IP del servidor y puerto del socket.

        """
        self.HEADER: int = 64
        self.PORT: int = 5555
        self.FORMAT: str = 'utf-8'
        self.DISCONNECT_MESSAGE: str = "!DISCONNECT"
        self.SERVER: str = "192.168.56.1"
        self.ADDR: tuple = (self.SERVER, self.PORT)

        self.start()

    def start(self)->None:
        """
        Inicia el socket del cliente, se conectara a la tupla con los datos del servidor
        :return: None
        """
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al tratar de conectarse al servidor: \n{exception}")


    def send(self, msg) -> None:
        """
        Trata de enviar un mensaje al servidor. Si no devuelve un error.
        :param msg: Mensaje a enviar al servidor
        :return: None
        """
        try:
            message = msg.encode(self.FORMAT)  # encode el mensaje con el formato utf-8
            msg_length = len(message)  # calcula cantidad de caracteres en el mensaje
            send_length = str(msg_length).encode(self.FORMAT) #chequea que los mensajes sean de 64bytes
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length) #se envia los mensajes
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