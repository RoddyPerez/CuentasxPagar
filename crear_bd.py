import sqlite3
import os

def crear_bd():
    db_path = os.path.join(os.path.dirname(__file__), 'cuentas_por_pagar.db')
    conn = sqlite3.connect(db_path)
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
            proveedor_id INTEGER NOT NULL,
            monto REAL NOT NULL,
            fecha_vencimiento DATE NOT NULL,
            descripcion TEXT,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)  
        )
    ''')

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS facturas (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           proveedor_id INTEGER,
           monto REAL,
           fecha TEXT,
           fecha_vencimiento TEXT,
           condiciones_pago TEXT,
           archivo TEXT,
           FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        )   
     ''')

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS pagos (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           factura_id INTEGER,
           monto REAL,
           fecha TEXT,
           metodo_pago TEXT,
           FOREIGN KEY (factura_id) REFERENCES facturas(id)
        )
  
     ''')

    conn.commit()
    conn.close()
    print("Base de datos y tablas creadas en la carpeta del proyecto.")

if __name__ == "__main__":
    crear_bd()
