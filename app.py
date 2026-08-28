from flask import Flask, render_template, redirect, url_for, flash, request
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_para_csrf_123456'

# ============================================================
# DATOS DE EJEMPLO (LISTAS CON NOMBRES CLAROS)
# ============================================================
lista_productos = [
    {'id': 1, 'nombre': 'RTX 4060', 'categoria': 'Tarjeta Grafica', 'precio': 350, 'stock': 10, 'descripcion': 'Tarjeta grafica de gama media'},
    {'id': 2, 'nombre': 'Ryzen 7 5800X', 'categoria': 'Procesador', 'precio': 320, 'stock': 5, 'descripcion': 'Procesador de 8 nucleos'},
    {'id': 3, 'nombre': 'SSD 1TB NVMe', 'categoria': 'Disco Duro', 'precio': 120, 'stock': 0, 'descripcion': 'Almacenamiento ultra rapido'},
]

lista_clientes = [
    {'id': 1, 'nombre': 'Carlos Perez', 'email': 'carlos@email.com', 'telefono': '0987654321', 'ciudad': 'Quito'},
    {'id': 2, 'nombre': 'Maria Gomez', 'email': 'maria@email.com', 'telefono': '0976543210', 'ciudad': 'Guayaquil'},
]

lista_proveedores = [
    {'id': 1, 'nombre': 'Intel Corporation', 'producto': 'Procesadores', 'contacto': 'Ana Ramirez', 'pais': 'USA'},
    {'id': 2, 'nombre': 'NVIDIA', 'producto': 'Tarjetas Graficas', 'contacto': 'Luis Torres', 'pais': 'USA'},
]

lista_facturas = [
    {'id': 1, 'cliente': 'Carlos Perez', 'producto': 'RTX 4060', 'cantidad': 2, 'total': 700, 'estado': 'Pagado'},
    {'id': 2, 'cliente': 'Maria Gomez', 'producto': 'Ryzen 7 5800X', 'cantidad': 1, 'total': 320, 'estado': 'Pendiente'},
]

contador_id = {'producto': 4, 'cliente': 3, 'proveedor': 3, 'factura': 3}

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
    global lista_productos
    
    if form.validate_on_submit():
        nuevo = {
            'id': contador_id['producto'],
            'nombre': form.nombre.data,
            'categoria': form.categoria.data,
            'precio': form.precio.data,
            'stock': form.stock.data,
            'descripcion': form.descripcion.data or ''
        }
        lista_productos.append(nuevo)
        contador_id['producto'] += 1
        flash('Producto agregado exitosamente', 'success')
        return redirect(url_for('productos'))
    
    return render_template('productos.html', lista_productos=lista_productos, form=form)

# ============================================================
# RUTA: CLIENTES
# ============================================================
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form = ClienteForm()
    global lista_clientes
    
    if form.validate_on_submit():
        nuevo = {
            'id': contador_id['cliente'],
            'nombre': form.nombre.data,
            'email': form.email.data,
            'telefono': form.telefono.data,
            'ciudad': form.ciudad.data
        }
        lista_clientes.append(nuevo)
        contador_id['cliente'] += 1
        flash('Cliente agregado exitosamente', 'success')
        return redirect(url_for('clientes'))
    
    return render_template('clientes.html', lista_clientes=lista_clientes, form=form)

# ============================================================
# RUTA: PROVEEDORES
# ============================================================
@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    form = ProveedorForm()
    global lista_proveedores
    
    if form.validate_on_submit():
        nuevo = {
            'id': contador_id['proveedor'],
            'nombre': form.nombre.data,
            'producto': form.producto.data,
            'contacto': form.contacto.data,
            'pais': form.pais.data
        }
        lista_proveedores.append(nuevo)
        contador_id['proveedor'] += 1
        flash('Proveedor agregado exitosamente', 'success')
        return redirect(url_for('proveedores'))
    
    return render_template('proveedores.html', lista_proveedores=lista_proveedores, form=form)

# ============================================================
# RUTA: FACTURACION
# ============================================================
@app.route('/facturacion', methods=['GET', 'POST'])
def facturacion():
    form = FacturacionForm()
    global lista_facturas
    
    if form.validate_on_submit():
        nuevo = {
            'id': contador_id['factura'],
            'cliente': form.cliente.data,
            'producto': form.producto.data,
            'cantidad': form.cantidad.data,
            'total': form.total.data,
            'estado': form.estado.data
        }
        lista_facturas.append(nuevo)
        contador_id['factura'] += 1
        flash('Factura agregada exitosamente', 'success')
        return redirect(url_for('facturacion'))
    
    return render_template('facturacion.html', lista_facturas=lista_facturas, form=form)

# ============================================================
# ELIMINAR REGISTROS
# ============================================================
@app.route('/eliminar/<tipo>/<int:id>')
def eliminar(tipo, id):
    global lista_productos, lista_clientes, lista_proveedores, lista_facturas
    
    if tipo == 'producto':
        lista_productos = [p for p in lista_productos if p['id'] != id]
    elif tipo == 'cliente':
        lista_clientes = [c for c in lista_clientes if c['id'] != id]
    elif tipo == 'proveedor':
        lista_proveedores = [p for p in lista_proveedores if p['id'] != id]
    elif tipo == 'factura':
        lista_facturas = [f for f in lista_facturas if f['id'] != id]
    
    flash('Registro eliminado', 'warning')
    return redirect(request.referrer or url_for('index'))

# ============================================================
# EJECUTAR
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)