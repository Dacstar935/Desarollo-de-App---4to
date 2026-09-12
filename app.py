from flask import Flask, render_template, redirect, url_for, flash, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import get_connection, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_123456'

# Inicializar la base de datos al arrancar
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
# PRODUCTOS - LISTAR (SELECT con JOIN)
# ============================================================
@app.route('/productos')
def productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, pr.nombre AS proveedor_nombre
        FROM productos p
        LEFT JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
    ''')
    lista_productos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    form = ProductoForm()
    return render_template('productos.html', lista_productos=lista_productos, form=form)

# ============================================================
# PRODUCTOS - AGREGAR (INSERT)
# ============================================================
@app.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.descripcion.data or ''
        ))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto agregado exitosamente', 'success')
    else:
        flash('Corrige los errores del formulario', 'danger')
    return redirect(url_for('productos'))

# ============================================================
# PRODUCTOS - EDITAR (formulario con datos actuales)
# ============================================================
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        form = ProductoForm()
        if form.validate_on_submit():
            cursor.execute('''
                UPDATE productos
                SET nombre = %s, categoria = %s, precio = %s, stock = %s, descripcion = %s
                WHERE id_producto = %s
            ''', (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                form.descripcion.data or '',
                id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos'))
    
    # GET: cargar datos actuales
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos'))
    
    form = ProductoForm(data=producto)
    return render_template('formulario_producto.html', form=form, producto=producto, editar=True)

# ============================================================
# PRODUCTOS - ELIMINAR (DELETE)
# ============================================================
@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Producto eliminado', 'warning')
    return redirect(url_for('productos'))

# ============================================================
# CLIENTES
# ============================================================
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if form.validate_on_submit():
        cursor.execute('''
            INSERT INTO clientes (nombre, email, telefono, ciudad)
            VALUES (%s, %s, %s, %s)
        ''', (form.nombre.data, form.email.data, form.telefono.data, form.ciudad.data))
        conn.commit()
        flash('Cliente agregado exitosamente', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('clientes'))
    
    cursor.execute('SELECT * FROM clientes ORDER BY id_cliente DESC')
    lista_clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', lista_clientes=lista_clientes, form=form)

@app.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id_cliente = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado', 'warning')
    return redirect(url_for('clientes'))

# ============================================================
# PROVEEDORES
# ============================================================
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if form.validate_on_submit():
        cursor.execute('''
            INSERT INTO proveedores (nombre, producto, contacto, pais)
            VALUES (%s, %s, %s, %s)
        ''', (form.nombre.data, form.producto.data, form.contacto.data, form.pais.data))
        conn.commit()
        flash('Proveedor agregado exitosamente', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('proveedores'))
    
    cursor.execute('SELECT * FROM proveedores ORDER BY id_proveedor DESC')
    lista_proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', lista_proveedores=lista_proveedores, form=form)

@app.route('/proveedores/eliminar/<int:id>')
def eliminar_proveedor(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id_proveedor = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor eliminado', 'warning')
    return redirect(url_for('proveedores'))

# ============================================================
# FACTURACION
# ============================================================
@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if form.validate_on_submit():
        cursor.execute('''
            INSERT INTO facturas (id_cliente, producto, cantidad, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        ''', (1, form.producto.data, form.cantidad.data, form.total.data, form.estado.data))
        conn.commit()
        flash('Factura agregada exitosamente', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('facturacion'))
    
    cursor.execute('SELECT * FROM facturas ORDER BY id_factura DESC')
    lista_facturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', lista_facturas=lista_facturas, form=form)

@app.route('/facturacion/eliminar/<int:id>')
def eliminar_factura(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id_factura = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Factura eliminada', 'warning')
    return redirect(url_for('facturacion'))

# ============================================================
# EJECUTAR
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)