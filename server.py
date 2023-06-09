import socket
import threading
from dateutil import parser
import datetime
import time

#estructura para guardar los datos de clientes + relojes
client_data = {}

class Server:
    """
    Contiene todos los metodos necesarios para inciar un servidor usando Hilos.
    """
    class Network:
        """
        Contiene los atributos del servidor para facil acceso en una subclase anidada. Tambien crea el socket principal
        """
        def __init__(self)-> None:
            """
            :var SERVER: Guarda la IP del servidor
            :var PORT: Numero de puerto a usar
            :var ADDR: Tupla con los datos de: ip y numero de puerto
            :var FORMAT: Formato de encode
            :var DISCONNECT_MESSAGE: mensaje para la desconección y cierre de sesion.
            :var HEADER: Numero de bytes usado para algoritmo logico = como no sabemos cual es el tamaño de cada mensaje, todos los mensajes seran de 64 bytes. Facilita el encode/decode.
            :var server: socket del servidor.
            """
            # obtener lan ip
            ips = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ips.connect(("8.8.8.8", 80))


            self.SERVER: str = ips.getsockname()[0]
            #cerrar  lan ips
            ips.close()

            self.PORT: int = 5555 #purto a usar
            self.ADDR: tuple = (self.SERVER, self.PORT)
            self.FORMAT: str = 'utf-8'
            self.DISCONNECT_MESSAGE: str= "!DISCONNECT"
            self.HEADER: int =64

            self.server: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.ADDR)
            self.initiateClocks()

        def startReceivingClockTime(self,connector, address):
            while True:
                # recibir el tiempo del reloj
                clock_time_string = connector.recv(1024).decode()
                clock_time = parser.parse(clock_time_string)
                clock_time_diff = datetime.datetime.now() - \
                                  clock_time

                client_data[address] = {
                    "clock_time": clock_time,
                    "time_difference": clock_time_diff,
                    "connector"	: connector
                }

                print("Client Data updated with:   "+ str(address),
                      end = "\n\n")
                time.sleep(5)


        #thread principal para crear un portal para aceptar clientes
        def startConnecting(self,master_server):
            # Actualizar relojes de los esclavos/clientes
            while True:
                # aceptando a los clientes
                master_slave_connector, addr = master_server.accept()
                slave_address = str(addr[0]) + ":" + str(addr[1])

                print(slave_address + " se conectó satisfacotiramente")

                current_thread = threading.Thread(
                    target=self.startReceivingClockTime,
                    args=(master_slave_connector,
                          slave_address,))
                current_thread.start()

        def getAverageClockDiff(self):

            current_client_data = client_data.copy()

            time_difference_list = list(client['time_difference']
                                        for client_addr, client
                                        in client_data.items())

            sum_of_clock_difference = sum(time_difference_list, \
                                          datetime.timedelta(0, 0))

            average_clock_difference = sum_of_clock_difference \
                                       / len(client_data)

            return average_clock_difference

        def synchronizeAllCloxks(self):

            while True:
                print("Nuevo ciclo de sincronizacion ha empezado")
                print("Nero de clientes sincronizados: " + \
                      str(len(client_data)))

                if len(client_data) > 0:

                    average_clock_difference = self.getAverageClockDiff()

                    for client_addr, client in client_data.items():
                        try:
                            synchronized_time = \
                                datetime.datetime.now() + \
                                average_clock_difference

                            client['connector'].send(str(
                                synchronized_time).encode())

                        except Exception as e:
                            print("Algo ocurrio " + \
                                  "mientras se enviaba los tiempos sincronizados " + \
                                  "atravez de: " + str(client_addr))

                else:
                    print("No client data." + \
                          " Synchronization not applicable.")

                print("\n\n")

                time.sleep(5)

        # metodo creea conecciones
        def initiateClocks(self):
            #creando conneccciones
            print("Creando las conecciones...\n")
            master_thread = threading.Thread(
                target=self.startConnecting,
                args=(self.server,))
            master_thread.start()

            #inicia sincronización
            print("Starting synchronization parallelly...\n")
            sync_thread = threading.Thread(
                target=self.synchronizeAllClocks,
                args=())
            sync_thread.start()



    def handle_client(self, conn, addr,n):
        """
        Metodo que maneja clientes, recibe mensajes y envia mensajes de confirmacion
        :param conn: connecion del socket.
        :param addr: tupla (ip,socket)
        :param n: Instancia de clase anidada "network"
        :return: None
        """
        print(f"[NUEVA CONNECCION] {addr} connectado.")
        primer_mensaje: bool = True
        esperando_dialogo: bool = True
        nombre_cliente:str =""

        connected: bool = True
        while connected:
            msg_length= conn.recv(n.HEADER).decode(n.FORMAT)

            if msg_length:
                if primer_mensaje == True:
                    msg_length = int(msg_length)
                    nombre_cliente = conn.recv(msg_length).decode(n.FORMAT)
                    primer_mensaje = False
                    print(f"Nombre del cliente connectado: {nombre_cliente}")
                    conn.send("[SERVIDOR] Conección establecida.".encode(n.FORMAT))
                else:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(n.FORMAT)
                    if msg == n.DISCONNECT_MESSAGE:
                        connected = False
                    print(f"Mensaje recibido del cliente:")
                    print(f"[{addr},{nombre_cliente}] {msg}")
                    msg: str = input(f"Escriba un mensaje para enviar al cliente {nombre_cliente}:\n")
                    conn.send(msg.encode(n.FORMAT))


    def start(self):
        """
        Incia el servidor mediante un try and catch.
        :return:  None
        """
        try:
            n = self.Network()
            n.server.listen()
            print(f"El servidor esta activo en la IP: {n.SERVER}\n")
            print(f"[Escuchando] Servidor esta escuchando...")
            while True:
                conn, addr = n.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, n))
                thread.start()
                print(f"[CONNECIONES ACTIVAS] {threading.active_count() - 1}")

        except Exception as e:
            exception: str = f"{type(e).__name__}: (e)"
            print(f"Error al Iniciar el servidor. El error fue: \n{exception}")



if __name__ =="__main__":
    print("[INICIANDO SERVIDOR] el servidor está iniciando....")
    s = Server()
    s.start()
