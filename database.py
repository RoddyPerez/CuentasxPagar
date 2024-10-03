import sqlite3
import os

# Asegúrate de que el archivo de la base de datos esté en la carpeta del proyecto
def conectar_bd():
    db_path = os.path.join(os.path.dirname(__file__), 'cuentas_por_pagar.db')
    return sqlite3.connect(db_path)

def crear_tablas():
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                email TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deudas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proveedor TEXT NOT NULL,
                monto REAL NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                descripcion TEXT
            )
        ''')
        conn.commit()
        conn.close()
