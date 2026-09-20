-- ============================================================
-- ESQUEMA DE LA BASE DE DATOS - TIENDA DE TECNOLOGÍA DC
-- ============================================================

CREATE DATABASE IF NOT EXISTS tienda_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE tienda_db;

-- ============================================================
-- TABLA: PROVEEDORES
-- ============================================================
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    producto VARCHAR(100) NOT NULL,
    contacto VARCHAR(100) NOT NULL,
    pais VARCHAR(50) NOT NULL
);

-- ============================================================
-- TABLA: PRODUCTOS (con FK a proveedores)
-- ============================================================
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
);

-- ============================================================
-- TABLA: CLIENTES
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    ciudad VARCHAR(50) NOT NULL
);

-- ============================================================
-- TABLA: FACTURAS (con FK a clientes)
-- ============================================================
CREATE TABLE IF NOT EXISTS facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    producto VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE SET NULL
);

-- ============================================================
-- DATOS DE EJEMPLO
-- ============================================================
INSERT INTO proveedores (nombre, producto, contacto, pais) VALUES
('Intel Corporation', 'Procesadores', 'Ana Ramirez', 'USA'),
('NVIDIA', 'Tarjetas Graficas', 'Luis Torres', 'USA'),
('Western Digital', 'Discos Duros', 'Elena Castro', 'Japon');

INSERT INTO productos (nombre, categoria, precio, stock, descripcion, id_proveedor) VALUES
('RTX 4060', 'Tarjeta Grafica', 350.00, 10, 'Tarjeta grafica de gama media', 2),
('Ryzen 7 5800X', 'Procesador', 320.00, 5, 'Procesador de 8 nucleos', 1),
('SSD 1TB NVMe', 'Disco Duro', 120.00, 0, 'Almacenamiento ultra rapido', 3);

INSERT INTO clientes (nombre, email, telefono, ciudad) VALUES
('Carlos Perez', 'carlos@email.com', '0987654321', 'Quito'),
('Maria Gomez', 'maria@email.com', '0976543210', 'Guayaquil');

INSERT INTO facturas (id_cliente, producto, cantidad, total, estado) VALUES
(1, 'RTX 4060', 2, 700.00, 'Pagado'),
(2, 'Ryzen 7 5800X', 1, 320.00, 'Pendiente');

-- ============================================================
-- TABLA: USUARIOS
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);