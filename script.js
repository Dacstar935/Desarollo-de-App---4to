document.addEventListener('DOMContentLoaded', function() {
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

    let total = 0;

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

    function actualizarContador() {
        contador.textContent = total;
        if (total === 0) {
            if (!document.getElementById('vacio')) {
                let p = document.createElement('p');
                p.id = 'vacio';
                p.className = 'text-muted text-center';
                p.textContent = 'No hay productos registrados';
                lista.appendChild(p);
            }
        } else {
            let p = document.getElementById('vacio');
            if (p) p.remove();
        }
    }

    function crearProducto(nombre, categoria, precio, descripcion) {
        let col = document.createElement('div');
        col.className = 'col-md-4 col-sm-6 mb-3';
        let card = document.createElement('div');
        card.className = 'card h-100';
        let body = document.createElement('div');
        body.className = 'card-body';
        let h5 = document.createElement('h5');
        h5.className = 'card-title text-primary';
        h5.textContent = nombre;
        let info = document.createElement('p');
        info.className = 'card-text small';
        info.innerHTML = '<strong>Categoria:</strong> ' + categoria + '<br><strong>Descripcion:</strong> ' + descripcion;
        let prec = document.createElement('p');
        prec.className = 'card-text';
        prec.textContent = precio > 0 ? 'Precio: $' + parseFloat(precio).toFixed(2) : 'Precio: No especificado';
        let btn = document.createElement('button');
        btn.className = 'btn btn-danger btn-sm mt-2';
        btn.textContent = 'Eliminar';
        btn.addEventListener('click', function() {
            if (confirm('¿Eliminar "' + nombre + '"?')) {
                col.remove();
                total--;
                actualizarContador();
            }
        });
        body.appendChild(h5);
        body.appendChild(info);
        body.appendChild(prec);
        body.appendChild(btn);
        card.appendChild(body);
        col.appendChild(card);
        return col;
    }

    n.addEventListener('input', validarNombre);
    n.addEventListener('blur', validarNombre);
    c.addEventListener('change', validarCategoria);
    c.addEventListener('blur', validarCategoria);
    p.addEventListener('input', validarPrecio);
    p.addEventListener('blur', validarPrecio);
    d.addEventListener('input', validarDescripcion);
    d.addEventListener('blur', validarDescripcion);

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!validarTodo()) {
            let alerta = document.createElement('div');
            alerta.className = 'alert alert-danger';
            alerta.textContent = 'Corrige los errores antes de registrar';
            form.prepend(alerta);
            setTimeout(function() { alerta.remove(); }, 3000);
            return;
        }
        lista.appendChild(crearProducto(n.value.trim(), c.value, parseFloat(p.value) || 0, d.value.trim()));
        total++;
        actualizarContador();
        mensajeExito.style.display = 'block';
        setTimeout(function() { mensajeExito.style.display = 'none'; }, 3000);
        form.reset();
        [n, c, p, d].forEach(function(campo) { campo.classList.remove('is-valid', 'is-invalid'); });
        [okN, okC, okP, okD].forEach(function(msg) { msg.style.display = 'none'; });
        [errN, errC, errP, errD].forEach(function(msg) { msg.style.display = 'none'; });
        n.focus();
    });

    actualizarContador();
});