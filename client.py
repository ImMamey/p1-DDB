
from timeit import default_timer as timer
import re
from dateutil import parser
import threading
import datetime
import socket
import time


'''Esta funcion-hilo se usa para enviar los datos de fecha desde el cliente.'''
def startSendingTime(slave_client):
    while True:
        # Se envia la informacion al servidor con los datos de la hora del cliente.
        slave_client.send(str(
            datetime.datetime.now()).encode())

        print("Tiempo actual ha sido enviado satisfactoriamente",
              end="\n\n")
        time.sleep(5)


'''Esta funcion-hilo se usa para recibir los datos de la hora desde el servidor.'''
def startReceivingTime(slave_client):
    while True:
        # Recibiendo y decodificando la informacion del servidor.
        Synchronized_time = parser.parse(
            slave_client.recv(1024).decode())

        print("El tiempo sincronizado en el cliente es: " + \
              str(Synchronized_time),
              end="\n\n")


"""Funcion usada para sincronizar el tiempo de procesamiento del cliente"""
def initiateSlaveClient(ip,port=5050):
    slave_client = socket.socket()

    #connecta el reloj del servidor
    slave_client.connect((ip, port))

    # Enviando la informacion del tiempo al servidor
    print("Enviando tiempo hacia el servidor\n")
    send_time_thread = threading.Thread(
        target=startSendingTime,
        args=(slave_client,))
    send_time_thread.start()

    # Enviando el tiempo sincronizado desde el servidor
    print("Recibiendo " + \
          "tiempo sincronizado desde el servidor\n")
    receive_time_thread = threading.Thread(
        target=startReceivingTime,
        args=(slave_client,))
    receive_time_thread.start()



if __name__ == '__main__':
    detente:bool = False
    while not detente:
        ip: str= input("Escriba el ip del servidor:\n")
        pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not pattern.match(ip):
            print("La ip no es válida. Intente nuevamente: \n")
        else:
            detente = True
    try:
        # Inicializar el cliente
        initiateSlaveClient(ip,port=5050)
    except Exception as e:
        exception: str = f"{type(e).__name__}: (e)"
        print(f"Error al iniciar el cliente esclavo. Por favor revisar los datos ingresados: \n{exception}")