import socket
from datetime import datetime
import sqlite3
from init_db import init_db


#Defino variables (o configuraciones globales) para luego utilizarlas
HOST = 'localhost'  # Dirección del servidor
PORT = 5000         # Puerto del servidor
BUFFER_SIZE = 1024  # Tamaño del buffer


#Función que inicializa el socket del servidor
def inicializar_socket():

    #Se crea un socket TCP (SOCK_STREAM)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Se vincula el socket a la dirección IP y puerto definidas al comienzo
    servidor.bind((HOST, PORT))

    #Establece la cantidad máxima de conexiones en espera
    servidor.listen(1)

    #Envía un mensaje de conexión exitosa 
    print(f"Servidor escuchando en {HOST}:{PORT}")
    return servidor


#Función que va a guardar el mensaje enviado por el cliente en la DB (recibe como parámetros la conexión a la DB, el mensaje y la IP del cliente)
def guardar_mensaje(db_conn, mensaje, ip_cliente):

    #Se define el tiempo actual en el cual se va a guardar el mensaje, que también se va a enviar como respuesta al cliente
    tiempo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #Ejecuta la sentencia SQL para guardar en la DB el mensaje enviado por el cliente junto con la información
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
        (mensaje, tiempo, ip_cliente)
    )
    db_conn.commit()

    #La función devuelve el tiempo en el que fue guardado el mensaje
    return tiempo


#Función encargada de manejar las conexiones en el servidor
def aceptar_conexiones(servidor, db_conn):

    #Si la conexión se realiza, espera a recibir los mensajes enviados por el socket del cliente
    while True:
        cliente_sock, cliente_addr = servidor.accept()
        print('Cliente conectado:', cliente_addr)

        while True:
            mensaje_bytes = cliente_sock.recv(BUFFER_SIZE)
            if not mensaje_bytes:
                break  # Significa que el cliente cerró la conexión

            mensaje = mensaje_bytes.decode()

            #Se llama a la función guardar_mensaje que devuelve el timestamp (la fecha y hora en la que se guardó el mensaje)
            try:
                timestamp = guardar_mensaje(db_conn, mensaje, cliente_addr[0])

            #Se manejan errores en caso de no poder guardar en la DB
            except Exception as e:
                print(f"Error al guardar en la base de datos: {e}")
                cliente_sock.sendall(f"Error de servidor: {e}".encode())
                continue

            #Se responde al cliente que el mensaje se recibió, junto con la fecha y hora en la que se guardó en la DB
            respuesta = f"Mensaje recibido: {timestamp}"
            cliente_sock.sendall(respuesta.encode())

        #En caso de no existir la conexión, porque el cliente se desconectó de alguna manera, si cierra la conexión con el socket
        cliente_sock.close()
        print('Cliente desconectado:', cliente_addr)

#Función que se encarga de correr el servidor
def run_server():

    #Se intenta conectar a la BD, inicializar el socket y ejecutar la función que acepta las conexiones
    try:
        db_conn = init_db()
        servidor = inicializar_socket()
        aceptar_conexiones(servidor, db_conn)

    #En caso de que uno o más de lo anterior no ocurra, se manejan los errores con las excepciones y se muestra el error
    except socket.error as e:
        print(f"Error de socket: {e}")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
    except Exception as e:
        print(f"Error general del servidor: {e}")
    
    #Una vez que el proceso finaliza, se cierra el socket y la conexión a la DB
    finally:
        if servidor:
            servidor.close()
        if db_conn:
            db_conn.close()

if __name__ == '__main__':
    run_server()
