import psycopg2
import psycopg2.extras
import os

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'Sima.2026',
    'database': 'tienda_db',
    'port': '5432'
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error: {e}")
        return None

def init_db():
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS proveedores (id_proveedor SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, producto VARCHAR(100) NOT NULL, contacto VARCHAR(100) NOT NULL, pais VARCHAR(50) NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS productos (id_producto SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, categoria VARCHAR(50) NOT NULL, precio DECIMAL(10,2) NOT NULL, stock INTEGER NOT NULL, descripcion TEXT, id_proveedor INTEGER REFERENCES proveedores(id_proveedor) ON DELETE SET NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS clientes (id_cliente SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, telefono VARCHAR(20) NOT NULL, ciudad VARCHAR(50) NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS facturas (id_factura SERIAL PRIMARY KEY, cliente VARCHAR(100) NOT NULL, producto VARCHAR(100) NOT NULL, cantidad INTEGER NOT NULL, total DECIMAL(10,2) NOT NULL, estado VARCHAR(20) NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, usuario VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL)')
    conn.commit()
    cursor.close()
    conn.close()
    print("Base de datos inicializada correctamente")