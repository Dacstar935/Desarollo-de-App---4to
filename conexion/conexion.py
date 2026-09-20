import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sima.2025',   
    'database': 'tienda_db'
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def init_db():
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            producto VARCHAR(100) NOT NULL,
            contacto VARCHAR(100) NOT NULL,
            pais VARCHAR(50) NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            stock INT NOT NULL,
            descripcion TEXT,
            id_proveedor INT,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
                ON DELETE SET NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            telefono VARCHAR(20) NOT NULL,
            ciudad VARCHAR(50) NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id_factura INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT,
            producto VARCHAR(100) NOT NULL,
            cantidad INT NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            estado VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                ON DELETE SET NULL
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Base de datos inicializada correctamente")