
from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

# Vector con los datos para guardar la informacion de clientes con datos de los relojes
client_data = {}

''' Esta funcion de hilos anidados se usa para recibir los datos del tiempo desde un cliente conectado'''

def startReceivingClockTime(connector, address)->None:
    '''
    :param connector: connecion del socket (objeto)
    :param address: la direccion del cliente/esclavo
    :return: None
    '''
    while True:
        # Estos datos son para recibir el tiempo de los relojes y guardarlos dentro del array "Client data"
        clock_time_string = connector.recv(1024).decode()
        clock_time = parser.parse(clock_time_string)
        clock_time_diff = datetime.datetime.now() - \
                          clock_time
        #se guardan los datos en un objeto dentro de el vector client_data (se usa luego para el algoritmo de berkley)
        client_data[address] = {
            "clock_time"	: clock_time,
            "time_difference" : clock_time_diff,
            "connector"	 : connector
        }

        print("Informacion de Clientes ha sido actualizada con:  "+ str(address),
              end = "\n\n")
        time.sleep(5)


''' Este es el hilo principal usado para abrir un partal para aceptar clientes dado un puerto especifico. '''
def startConnecting(master_server)->None:
    '''

    :param master_server: Objeto de tipo socket
    :return: None
    '''
    # Actualiza los tiempos de reloj de cada esclavo/clientes
    # siguiente ciclo acepta cada cliente/esclavo que intente conectarse
    while True:
        master_slave_connector, addr = master_server.accept()
        slave_address = str(addr[0]) + ":" + str(addr[1])

        print(slave_address + " se ha conectado satisfacotiramente.")

        current_thread = threading.Thread(
            target = startReceivingClockTime,
            args = (master_slave_connector,
                    slave_address, ))
        current_thread.start()



"""Subrutina para guardar la media entre los relojes. Esta subrutina ejecuta al algoritmo de Berkeley."""
def getAverageClockDiff():
    #Creamos una copia del vector con la informacion de los relojes
    current_client_data = client_data.copy()

    #creamos una lista con la diferencia de tiempos por cada objeto de clientes.
    time_difference_list = list(client['time_difference']
                                for client_addr, client
                                in client_data.items())

    #Hacemos una sumatoria de los mismos
    sum_of_clock_difference = sum(time_difference_list, \
                                  datetime.timedelta(0, 0))
    #creamos la media de todos los relojes.
    average_clock_difference = sum_of_clock_difference \
                               / len(client_data)
    #devolvemos la media de los relojes
    return average_clock_difference


''' Este hilo se usa para genera ciclos de sincronizacion en la red. '''
def synchronizeAllClocks():

    while True:

        print("Nuevo ciclo de sincronización ha empezado.")
        print("Numero de clientes a ser sincronizados:" + \
              str(len(client_data)))

        #empieza la sincronización por cada item cliente dentro del vector de clientes.
        if len(client_data) > 0:
            #guardamos el valor de la media de los relojes
            average_clock_difference = getAverageClockDiff()

            for client_addr, client in client_data.items():
                # por cada cliente, enviamos el valor del reloj sincronizados
                try:
                    synchronized_time = \
                        datetime.datetime.now() + \
                        average_clock_difference

                    client['connector'].send(str(
                        synchronized_time).encode())

                except Exception as e:
                    print("Algo ocurrió cuando" + \
                          "se intento enviar el tiempo sincronizado " + \
                          "hacia: " + str(client_addr))

        else :
            print("No hay informacion de clientes" + \
                  " La sincronización no es aplicable.")

        print("\n\n")

        time.sleep(5)


"""Esta funcion se usa para inciar el reloj del servidor/maestro"""
def initiateClockServer(port = 5050):
    #aqui creamos el socket para nuestro servidor/nodo maestro.

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()


    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET,
                             socket.SO_REUSEADDR, 1)

    print("[INICIANDO SERVIDOR] el servidor ha iniciado....\n")
    print(f"El servidor ha iniciado en la siguiente ip: ", IP)
    master_server.bind((IP, port))

    # Esperando conecciones
    print(f"[Escuchando] Servidor esta escuchando...")
    master_server.listen(10)
    print("El reloj del servidor ah iniciado...\n")

    # start making connections
    print("Creando conneciones\n")
    master_thread = threading.Thread(
        target = startConnecting,
        args = (master_server, ))
    master_thread.start()

    # start synchronization
    print("Iniciando conneciones paralelas..\n")
    sync_thread = threading.Thread(
        target = synchronizeAllClocks,
        args = ())
    sync_thread.start()

import socket


"""Funcion usada para obtener el IP de la maquina actual para la creacion del socket."""



# Driver function
if __name__ == '__main__':
    print("[INICIANDO SERVIDOR] el servidor esta iniciando")
    # Trigger the Clock Server
    initiateClockServer(port = 5050)
