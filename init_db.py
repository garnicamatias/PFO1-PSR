import sqlite3

DB_FILE = 'mensajes.db'

#Define la función que va a inicializar la base de datos
def init_db():

    #Inicializa la base de datos SQLite y crea la tabla si no existe.
    #Campos: id (INTEGER PRIMARY KEY), contenido (TEXT), fecha_envio (TEXT), ip_cliente (TEXT)
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
            '''
        )
        conn.commit()
        print(f"Base de datos inicializada correctamente.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise


if __name__ == '__main__':
    #Permite crear el archivo de la base de datos ejecutando este módulo directamente
    init_db()