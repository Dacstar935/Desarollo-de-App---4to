from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm
from conexion.conexion import get_connection, init_db
from models import Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_123456'

# ============================================================
# CONFIGURACIÓN DE FLASK-LOGIN
# ============================================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder'

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return Usuario(user['id'], user['usuario'], user['password'])
    return None

# Inicializar base de datos
init_db()

# ============================================================
# LOGIN
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], form.password.data):
            usuario_obj = Usuario(user['id'], user['usuario'], user['password'])
            login_user(usuario_obj)
            flash('Bienvenido ' + user['usuario'], 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html', form=form)

# ============================================================
# REGISTRO DE USUARIOS
# ============================================================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = UsuarioForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (form.usuario.data,))
        existe = cursor.fetchone()

        if existe:
            flash('El usuario ya existe', 'danger')
            cursor.close()
            conn.close()
            return render_template('registro.html', form=form)

        password_hash = generate_password_hash(form.password.data)
        cursor.execute('INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
                       (form.usuario.data, password_hash))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)

# ============================================================
# LOGOUT
# ============================================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

# ============================================================
# DASHBOARD (protegido)
# ============================================================
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route('/')
def index():
    nombre_tienda = "Tienda de Tecnologia DC"
    anio = 2026
    return render_template('index.html', nombre_tienda=nombre_tienda, anio=anio)

# ============================================================
# PRODUCTOS (protegido)
# ============================================================
@app.route('/productos')
@login_required
def productos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
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

@app.route('/productos/agregar', methods=['POST'])
@login_required
def agregar_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock, descripcion)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.descripcion.data or ''))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto agregado exitosamente', 'success')
    return redirect(url_for('productos'))

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if request.method == 'POST':
        form = ProductoForm()
        if form.validate_on_submit():
            cursor.execute('''
                UPDATE productos SET nombre=%s, categoria=%s, precio=%s, stock=%s, descripcion=%s
                WHERE id_producto=%s
            ''', (form.nombre.data, form.categoria.data, form.precio.data, form.stock.data, form.descripcion.data or '', id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Producto actualizado', 'success')
            return redirect(url_for('productos'))
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    form = ProductoForm(data=producto)
    return render_template('formulario_producto.html', form=form, producto=producto)

@app.route('/productos/eliminar/<int:id>')
@login_required
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
# CLIENTES (protegido)
# ============================================================
@app.route('/clientes', methods=['GET', 'POST'])
@login_required
def clientes():
    form = ClienteForm()
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if form.validate_on_submit():
        cursor.execute('INSERT INTO clientes (nombre, email, telefono, ciudad) VALUES (%s, %s, %s, %s)',
                       (form.nombre.data, form.email.data, form.telefono.data, form.ciudad.data))
        conn.commit()
        flash('Cliente agregado', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('clientes'))
    cursor.execute('SELECT * FROM clientes ORDER BY id_cliente DESC')
    lista_clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', lista_clientes=lista_clientes, form=form)

@app.route('/clientes/eliminar/<int:id>')
@login_required
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
# PROVEEDORES (protegido)
# ============================================================
@app.route('/proveedores', methods=['GET', 'POST'])
@login_required
def proveedores():
    form = ProveedorForm()
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if form.validate_on_submit():
        cursor.execute('INSERT INTO proveedores (nombre, producto, contacto, pais) VALUES (%s, %s, %s, %s)',
                       (form.nombre.data, form.producto.data, form.contacto.data, form.pais.data))
        conn.commit()
        flash('Proveedor agregado', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('proveedores'))
    cursor.execute('SELECT * FROM proveedores ORDER BY id_proveedor DESC')
    lista_proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', lista_proveedores=lista_proveedores, form=form)

@app.route('/proveedores/eliminar/<int:id>')
@login_required
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
# FACTURACION (protegido)
# ============================================================
@app.route('/facturacion', methods=['GET', 'POST'])
@login_required
def facturacion():
    form = FacturacionForm()
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if form.validate_on_submit():
        cursor.execute('''
            INSERT INTO facturas (cliente, producto, cantidad, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        ''', (form.cliente.data, form.producto.data, form.cantidad.data, form.total.data, form.estado.data))
        conn.commit()
        flash('Factura agregada', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('facturacion'))
    cursor.execute('SELECT * FROM facturas ORDER BY id_factura DESC')
    lista_facturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', lista_facturas=lista_facturas, form=form)

@app.route('/facturacion/eliminar/<int:id>')
@login_required
def eliminar_factura(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id_factura = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Factura eliminada', 'warning')
    return redirect(url_for('facturacion'))

@app.route('/test-navbar')
def test_navbar():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="#">Tienda DC</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navMenu">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item"><a class="nav-link" href="#">Inicio</a></li>
                        <li class="nav-item"><a class="nav-link" href="#">Productos</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container mt-4">
            <h1>Test Navbar</h1>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

# ============================================================
# EJECUTAR
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)