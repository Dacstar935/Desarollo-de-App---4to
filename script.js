// =============================================================
// DATOS INICIALES (arreglo de productos)
// =============================================================
let productos = [];

// =============================================================
// REFERENCIAS AL DOM
// =============================================================
const form = document.getElementById('formProducto');
const n = document.getElementById('nombre');
const c = document.getElementById('categoria');
const p = document.getElementById('precio');
const d = document.getElementById('descripcion');
const lista = document.getElementById('listaProductos');
const contador = document.getElementById('contador');
const mensajeExito = document.getElementById('mensajeExito');

const errN = document.getElementById('errNombre');
const errC = document.getElementById('errCategoria');
const errP = document.getElementById('errPrecio');
const errD = document.getElementById('errDescripcion');
const okN = document.getElementById('okNombre');
const okC = document.getElementById('okCategoria');
const okP = document.getElementById('okPrecio');
const okD = document.getElementById('okDescripcion');

// =============================================================
// VALIDACIONES (Semana 6)
// =============================================================
function validarNombre() {
    const valor = n.value.trim();
    if (valor.length >= 3) {
        n.classList.remove('is-invalid');
        n.classList.add('is-valid');
        errN.style.display = 'none';
        okN.style.display = 'block';
        return true;
    } else {
        n.classList.remove('is-valid');
        n.classList.add('is-invalid');
        errN.style.display = 'block';
        okN.style.display = 'none';
        return false;
    }
}

function validarCategoria() {
    if (c.value !== '') {
        c.classList.remove('is-invalid');
        c.classList.add('is-valid');
        errC.style.display = 'none';
        okC.style.display = 'block';
        return true;
    } else {
        c.classList.remove('is-valid');
        c.classList.add('is-invalid');
        errC.style.display = 'block';
        okC.style.display = 'none';
        return false;
    }
}

function validarPrecio() {
    if (p.value === '' || parseFloat(p.value) >= 0) {
        p.classList.remove('is-invalid');
        p.classList.add('is-valid');
        errP.style.display = 'none';
        okP.style.display = 'block';
        return true;
    } else {
        p.classList.remove('is-valid');
        p.classList.add('is-invalid');
        errP.style.display = 'block';
        okP.style.display = 'none';
        return false;
    }
}

function validarDescripcion() {
    const valor = d.value.trim();
    if (valor.length >= 10) {
        d.classList.remove('is-invalid');
        d.classList.add('is-valid');
        errD.style.display = 'none';
        okD.style.display = 'block';
        return true;
    } else {
        d.classList.remove('is-valid');
        d.classList.add('is-invalid');
        errD.style.display = 'block';
        okD.style.display = 'none';
        return false;
    }
}

function validarTodo() {
    return validarNombre() && validarCategoria() && validarPrecio() && validarDescripcion();
}

// =============================================================
// RENDERIZADO DINÁMICO (Semana 7)
// =============================================================

// Función para renderizar todos los productos
function renderizarProductos() {
    // Limpiar la lista
    lista.innerHTML = '';

    // CONDICIÓN: Si no hay productos, mostrar mensaje
    if (productos.length === 0) {
        const vacio = document.createElement('p');
        vacio.className = 'text-muted text-center';
        vacio.textContent = 'No hay productos registrados';
        lista.appendChild(vacio);
        contador.textContent = '0';
        return;
    }

    // ACTUALIZAR CONTADOR
    contador.textContent = productos.length;

    // RECORRER EL ARREGLO Y CREAR TARJETAS
    productos.forEach(function(producto, index) {
        const col = document.createElement('div');
        col.className = 'col-md-4 col-sm-6 mb-3 producto-card';

        const card = document.createElement('div');
        card.className = 'card h-100';

        const body = document.createElement('div');
        body.className = 'card-body';

        const titulo = document.createElement('h5');
        titulo.className = 'card-title text-primary';
        titulo.textContent = producto.nombre;

        const info = document.createElement('p');
        info.className = 'card-text small';
        info.innerHTML = '<strong>Categoria:</strong> ' + producto.categoria + '<br><strong>Descripcion:</strong> ' + producto.descripcion;

        const precio = document.createElement('p');
        precio.className = 'card-text';
        precio.textContent = producto.precio > 0 ? 'Precio: $' + parseFloat(producto.precio).toFixed(2) : 'Precio: No especificado';

        const btn = document.createElement('button');
        btn.className = 'btn btn-danger btn-sm mt-2';
        btn.textContent = 'Eliminar';
        btn.addEventListener('click', function() {
            if (confirm('¿Eliminar "' + producto.nombre + '"?')) {
                // Eliminar del arreglo
                productos.splice(index, 1);
                // Re-renderizar
                renderizarProductos();
            }
        });

        body.appendChild(titulo);
        body.appendChild(info);
        body.appendChild(precio);
        body.appendChild(btn);
        card.appendChild(body);
        col.appendChild(card);
        lista.appendChild(col);
    });
}

// =============================================================
// EVENTOS EN TIEMPO REAL (Semana 6)
// =============================================================
n.addEventListener('input', validarNombre);
n.addEventListener('blur', validarNombre);
c.addEventListener('change', validarCategoria);
c.addEventListener('blur', validarCategoria);
p.addEventListener('input', validarPrecio);
p.addEventListener('blur', validarPrecio);
d.addEventListener('input', validarDescripcion);
d.addEventListener('blur', validarDescripcion);

// =============================================================
// EVENTO SUBMIT (Registrar nuevo producto)
// =============================================================
form.addEventListener('submit', function(e) {
    e.preventDefault();

    // Validar
    if (!validarTodo()) {
        let alerta = document.createElement('div');
        alerta.className = 'alert alert-danger';
        alerta.textContent = 'Corrige los errores antes de registrar';
        form.prepend(alerta);
        setTimeout(function() { alerta.remove(); }, 3000);
        return;
    }

    // Crear objeto producto
    const nuevoProducto = {
        nombre: n.value.trim(),
        categoria: c.value,
        precio: parseFloat(p.value) || 0,
        descripcion: d.value.trim()
    };

    // Agregar al arreglo
    productos.push(nuevoProducto);

    // Renderizar nuevamente
    renderizarProductos();

    // Mostrar mensaje de éxito
    mensajeExito.style.display = 'block';
    setTimeout(function() { mensajeExito.style.display = 'none'; }, 3000);

    // Limpiar formulario
    form.reset();
    [n, c, p, d].forEach(function(campo) { campo.classList.remove('is-valid', 'is-invalid'); });
    [okN, okC, okP, okD].forEach(function(msg) { msg.style.display = 'none'; });
    [errN, errC, errP, errD].forEach(function(msg) { msg.style.display = 'none'; });
    n.focus();
});

// =============================================================
// CARGA INICIAL (con datos de ejemplo)
// =============================================================
// Datos iniciales para mostrar que funciona
const datosEjemplo = [
    { nombre: 'RTX 4060', categoria: 'Tarjeta Grafica', precio: 350, descripcion: 'Tarjeta grafica de gama media' },
    { nombre: 'Ryzen 7 5800X', categoria: 'Procesador', precio: 320, descripcion: 'Procesador de 8 nucleos para gaming' },
    { nombre: 'SSD 1TB NVMe', categoria: 'Disco Duro', precio: 120, descripcion: 'Almacenamiento ultra rapido' }
];

// Cargar datos de ejemplo
productos = datosEjemplo;
renderizarProductos();