import socket

#Defino variables (o configuraciones globales) para luego utilizarlas
HOST = 'localhost'  # Dirección del servidor
PORT = 5000         # Puerto del servidor
BUFFER_SIZE = 1024  # Tamaño del buffer

#Función que corre al cliente
def run_client():

    #Se crea un socket TCP (SOCK_STREAM) del lado del cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
            #Se intenta conectar el socket del cliente con el socket del servidor a través de la dirección y el puerto establecios inicialmente 
            cliente.connect((HOST, PORT))
            print(f"Conectado a {HOST}:{PORT}")

            #Se manejan errores en caso de no lograr conectarse
    except socket.error as e:
            print(f"No se pudo conectar al servidor: {e}")
            return

    while True:
            #Una vez realizada la conexión, se espera que se escriba un mensaje
            mensaje = input("Escribí un mensaje (o 'éxito' para terminar): ")
            #Si se escribe 'éxito', la conexión del socket se cierra
            if mensaje == 'éxito':
                print("Cerrando cliente...")
                cliente.close()
                break

            try:
                #Caso contrario, se envía el mensaje al servidor
                cliente.sendall(mensaje.encode())

                #Se recibe la respuesta, la cual es la fecha y hora en la que se guardo el mensaje en la DB
                respuesta = cliente.recv(BUFFER_SIZE).decode()
                print('Respuesta del servidor:', respuesta)

                #Caso contrario, se manejan los errores
            except socket.error as e:
                print(f"Error durante la comunicación: {e}")
                break


if __name__ == '__main__':
    run_client()