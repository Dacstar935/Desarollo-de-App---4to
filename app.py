from flask import Flask, render_template, redirect, url_for, flash, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_123456'

# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================
DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'tienda.db')

def get_db():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea las tablas si no existen"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            descripcion TEXT
        )
    ''')
    
    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            ciudad TEXT NOT NULL
        )
    ''')
    
    # Tabla de proveedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            producto TEXT NOT NULL,
            contacto TEXT NOT NULL,
            pais TEXT NOT NULL
        )
    ''')
    
    # Tabla de facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

# Inicializar la base de datos al arrancar la aplicación
init_db()

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route('/')
def index():
    nombre_tienda = "Tienda de Tecnologia DC"
    anio = 2026
    return render_template('index.html', nombre_tienda=nombre_tienda, anio=anio)

# ============================================================
# RUTA: PRODUCTOS
# ============================================================
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()
    
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock, descripcion)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.descripcion.data or ''
        ))
        conn.commit()
        conn.close()
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('productos'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos ORDER BY id DESC')
    lista_productos = cursor.fetchall()
    conn.close()
    
    return render_template('productos.html', lista_productos=lista_productos, form=form)

# ============================================================
# ELIMINAR PRODUCTO
# ============================================================
@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado', 'warning')
    return redirect(url_for('productos'))

# ============================================================
# RUTA: CLIENTES
# ============================================================
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, email, telefono, ciudad)
            VALUES (?, ?, ?, ?)
        ''', (
            form.nombre.data,
            form.email.data,
            form.telefono.data,
            form.ciudad.data
        ))
        conn.commit()
        conn.close()
        flash('Cliente agregado exitosamente', 'success')
        return redirect(url_for('clientes'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
    lista_clientes = cursor.fetchall()
    conn.close()
    
    return render_template('clientes.html', lista_clientes=lista_clientes, form=form)

# ============================================================
# ELIMINAR CLIENTE
# ============================================================
@app.route('/eliminar_cliente/<int:id>')
def eliminar_cliente(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Cliente eliminado', 'warning')
    return redirect(url_for('clientes'))

# ============================================================
# RUTA: PROVEEDORES
# ============================================================
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedores (nombre, producto, contacto, pais)
            VALUES (?, ?, ?, ?)
        ''', (
            form.nombre.data,
            form.producto.data,
            form.contacto.data,
            form.pais.data
        ))
        conn.commit()
        conn.close()
        flash('Proveedor agregado exitosamente', 'success')
        return redirect(url_for('proveedores'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores ORDER BY id DESC')
    lista_proveedores = cursor.fetchall()
    conn.close()
    
    return render_template('proveedores.html', lista_proveedores=lista_proveedores, form=form)

# ============================================================
# ELIMINAR PROVEEDOR
# ============================================================
@app.route('/eliminar_proveedor/<int:id>')
def eliminar_proveedor(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Proveedor eliminado', 'warning')
    return redirect(url_for('proveedores'))

# ============================================================
# RUTA: FACTURACION
# ============================================================
@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (cliente, producto, cantidad, total, estado)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            form.cliente.data,
            form.producto.data,
            form.cantidad.data,
            form.total.data,
            form.estado.data
        ))
        conn.commit()
        conn.close()
        flash('Factura agregada exitosamente', 'success')
        return redirect(url_for('facturacion'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas ORDER BY id DESC')
    lista_facturas = cursor.fetchall()
    conn.close()
    
    return render_template('facturacion.html', lista_facturas=lista_facturas, form=form)

# ============================================================
# ELIMINAR FACTURA
# ============================================================
@app.route('/eliminar_factura/<int:id>')
def eliminar_factura(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Factura eliminada', 'warning')
    return redirect(url_for('facturacion'))

# ============================================================
# EJECUTAR
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)