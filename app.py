from flask import Flask, render_template

app = Flask(__name__)

# ============================================================
# RUTA PRINCIPAL
# ============================================================
@app.route('/')
def index():
    # Variable simple
    nombre_tienda = "Tienda de Tecnologia DC"
    anio = 2026
    return render_template('index.html', nombre_tienda=nombre_tienda, anio=anio)

# ============================================================
# RUTA: PRODUCTOS (con datos dinámicos)
# ============================================================
@app.route('/productos')
def productos():
    # Lista de diccionarios con productos (stock incluido)
    lista_productos = [
        {'id': 1, 'nombre': 'RTX 4060', 'categoria': 'Tarjeta Grafica', 'precio': 350, 'stock': 10},
        {'id': 2, 'nombre': 'Ryzen 7 5800X', 'categoria': 'Procesador', 'precio': 320, 'stock': 5},
        {'id': 3, 'nombre': 'SSD 1TB NVMe', 'categoria': 'Disco Duro', 'precio': 120, 'stock': 0},
        {'id': 4, 'nombre': 'Memoria RAM 16GB', 'categoria': 'Memoria RAM', 'precio': 80, 'stock': 15},
        {'id': 5, 'nombre': 'Fuente 750W', 'categoria': 'Fuente de Poder', 'precio': 150, 'stock': 3},
        {'id': 6, 'nombre': 'Monitor 24"', 'categoria': 'Monitor', 'precio': 200, 'stock': 0}
    ]
    # Variable simple para usar en la plantilla
    titulo_pagina = "Lista de Productos"
    return render_template('productos.html', productos=lista_productos, titulo_pagina=titulo_pagina)

# ============================================================
# RUTA: CLIENTES
# ============================================================
@app.route('/clientes')
def clientes():
    lista_clientes = [
        {'id': 1, 'nombre': 'Carlos Perez', 'email': 'carlos@email.com', 'telefono': '0987654321', 'ciudad': 'Quito'},
        {'id': 2, 'nombre': 'Maria Gomez', 'email': 'maria@email.com', 'telefono': '0976543210', 'ciudad': 'Guayaquil'},
        {'id': 3, 'nombre': 'Juan Lopez', 'email': 'juan@email.com', 'telefono': '0965432109', 'ciudad': 'Cuenca'}
    ]
    return render_template('clientes.html', clientes=lista_clientes)

# ============================================================
# RUTA: PROVEEDORES
# ============================================================
@app.route('/proveedores')
def proveedores():
    lista_proveedores = [
        {'id': 1, 'nombre': 'Intel Corporation', 'producto': 'Procesadores', 'contacto': 'Ana Ramirez', 'pais': 'USA'},
        {'id': 2, 'nombre': 'NVIDIA', 'producto': 'Tarjetas Graficas', 'contacto': 'Luis Torres', 'pais': 'USA'},
        {'id': 3, 'nombre': 'Western Digital', 'producto': 'Discos Duros', 'contacto': 'Elena Castro', 'pais': 'Japon'}
    ]
    return render_template('proveedores.html', proveedores=lista_proveedores)

# ============================================================
# RUTA: FACTURACION
# ============================================================
@app.route('/facturacion')
def facturacion():
    lista_facturas = [
        {'id': 1, 'cliente': 'Carlos Perez', 'producto': 'RTX 4060', 'cantidad': 2, 'total': 700, 'estado': 'Pagado'},
        {'id': 2, 'cliente': 'Maria Gomez', 'producto': 'Ryzen 7 5800X', 'cantidad': 1, 'total': 320, 'estado': 'Pendiente'},
        {'id': 3, 'cliente': 'Juan Lopez', 'producto': 'SSD 1TB NVMe', 'cantidad': 3, 'total': 360, 'estado': 'Pagado'},
        {'id': 4, 'cliente': 'Carlos Perez', 'producto': 'Monitor 24"', 'cantidad': 1, 'total': 200, 'estado': 'Cancelado'}
    ]
    return render_template('facturacion.html', facturas=lista_facturas)

# ============================================================
# EJECUTAR
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)