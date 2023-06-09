import socket
import re
import sys
from dateutil import parser
import time
import datetime
import threading

class Client:
    """
    Contiene todos los metodos para el cliente.
    """
    def __init__(self,ip) -> None:
        """
        :var HEADER: Numero de bytes usado para algoritmo logico = como no sabemos cual es el tamaño de cada mensaje,
        todos los mensajes seran de 64 bytes. Facilita el encode/decode.
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
        self.SERVER: str = ip #"192.168.56.1"
        self.ADDR: tuple = (self.SERVER, self.PORT)

        self.start()

#Funcion en hilo usada para enviar el tiempo desde el lado del cliente
    def startSendingTime(self,slave_client):
        while True:
            # proveee al servidor con los datos del reloj del cliente
            slave_client.send(str(datetime.datetime.now()).encode())

            print("Tiempo actua enviado satisfactoriamente",
                  end="\n\n")
            time.sleep(60)

    #Funcion en hilo para recibir el tiempo sincronizado del servidor.
    def startReceivingTime(slave_client):
        while True:
            # receive data from the server
            Synchronized_time = parser.parse(
                slave_client.recv(1024).decode())

            print("El tiempo sincronizado del cliente es: " + \
                  str(Synchronized_time),
                  end="\n\n")


    def start(self)->None:
        """
        Inicia el socket del cliente, se conectara a la tupla con los datos del servidor
        :return: None
        """
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)

            #Empieza a enviar tiempo del cliente actual al servidor
            print("Empezando a recibir tiempo desde el servidor.\n")
            send_time_thread = threading.Thread(
            target=self.startSendingTime,
            args=(self.client,))
            send_time_thread.start()

            # empieza a recibir el tiempo sincronizado desde el servidor.
            print("Empezando a recibir el tiempo desde el servidor " + \
                  "Tiempo sincronizado del servidor\n")
            receive_time_thread = threading.Thread(
                target=self.startReceivingTime,
                args=(self.client,))
            receive_time_thread.start()

        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al tratar de conectarse al servidor: \n{exception}")
            sys.exit("El cliente se cerrará despues de el log....")


    def send(self, msg) -> None:
        """
        Trata de enviar un mensaje al servidor. Si no devuelve un error.
        :param msg: Mensaje a enviar al servidor
        :return: None
        """
        try:
            message = msg.encode(self.FORMAT)  #encode el mensaje con el formato utf-8
            msg_length = len(message)  #calcula cantidad de caracteres en el mensaje
            send_length = str(msg_length).encode(self.FORMAT) #chequea que los mensajes sean de 64bytes
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length) #se envia los mensajes
            self.client.send(message)
            print(self.client.recv(2048).decode(self.FORMAT))
        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al enviar el mensaje: \n{exception}")


if __name__ == "__main__":
    detente: bool = False

    while not detente:
        ip: str= input("Escriba el ip del servidor:\n")
        pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not pattern.match(ip):
            print("La ip no es válida. Intente nuevamente: \n")
        else:
            detente = True

    cl = Client(ip)
    #nombre: str = input("Escriba el nombre del cliente:\n")
    #cl.send(str(nombre))
    detente: bool = False

    #TODO: Esto no va,
    #while not detente:
    #    msg: str = input("Escriba un mensaje para enviar al Servidor (escriba \"n\" para detener)\n")
    #    if msg=="n":
    #        detente=True
    #        cl.send(cl.DISCONNECT_MESSAGE)
    #    else:
    #        cl.send(str(msg))
    #        print(f"[Enviado] Mensaje enviado al servidor: {msg}")